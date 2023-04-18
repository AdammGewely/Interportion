import os


def get_directory_size(directory):
    total_size = 0
    for path, dirs, files in os.walk(directory):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size


last = 0
while True:
    directory_path = "/home/adamgewely/Documents/Interportion/data"
    directory_size = get_directory_size(directory_path)
    if directory_size != last:
        print(f"{directory_size}")
    last = directory_size
