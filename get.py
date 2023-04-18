import os
import threading
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

# List of allowed websites
ALLOWED_WEBSITES = ["youtube.com"]

# Dictionary to store robots.txt file for each domain
ROBOTS_DICT = {}


# Function to check if a URL is allowed
def is_allowed(url):
    for website in ALLOWED_WEBSITES:
        if website in url:
            # Check if robots.txt is allowed for this URL
            if website not in ROBOTS_DICT:
                robots_url = f"https://{website}/robots.txt"
                rp = RobotFileParser()
                try:
                    rp.set_url(robots_url)
                    rp.read()
                    ROBOTS_DICT[website] = rp
                except:
                    pass
            if website in ROBOTS_DICT:
                return ROBOTS_DICT[website].can_fetch("*", url)
            else:
                return True
    return False


def load_visited_urls():  # Let's not get into this now
    return set()


def save_visited_urls():  # Let's not get into this now
    pass


def format_size(size):
    if size < 1000:
        return f"{size}B"
    elif size < 1000_000:
        return f"{size / 1000}KB"
    elif size < 1000_000_000:
        return f"{size / 1000_000}MB"
    elif size < 1000_000_000_000:
        return f"{size / 1000_000_000}GB"
    else:
        return f"{size / 1000_000_000}TB"


visited_urls = load_visited_urls()

NUM_THREADS = 40  # You may want to lower this for slower devices or different policies
threads = []


def crawl_links(url, depth=0, max_depth=20):
    try:
        # Check if URL is allowed
        if not is_allowed(url):
            return

        # Check if URL has already been visited
        if url in visited_urls:
            return
        visited_urls.add(url)

        # Make a directory for the website if it doesn't exist
        domain = url.split("//")[-1].split("/")[0]
        directory = os.path.join("data", domain)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Download HTML
        response = requests.get(url)
        print(f"Visited URL {url} at depth {depth}.")
        soup = BeautifulSoup(response.content, "html.parser")

        # Save HTML to file
        filename = os.path.join(directory, f"{depth}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Saved {filename}.")
        size = format_size(os.path.getsize(filename))
        print(f"Size: {size}.")

        # Recursively crawl links
        if depth < max_depth:
            links = soup.find_all("a")
            for link in links:
                href = link.get("href")
                if href and href.startswith("http"):
                    if len(threads) < NUM_THREADS:
                        threads.append(
                            threading.Thread(target=lambda: crawl_links(href, depth + 1, max_depth))
                        )
                        threads[-1].start()
                    else:
                        crawl_links(href, depth + 1, max_depth)

    except requests.exceptions.ConnectionError:
        return
    finally:
        save_visited_urls()


# Main function
if __name__ == "__main__":
    for i in ALLOWED_WEBSITES:
        crawl_links(f"https://{i}")
