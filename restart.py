import os

print("WARNING: This will wipe all progress (Which can be useful for a different depth adjusted etc.),")
warning = input("please make sure you want to proceed (Y/n): ")
if warning.lower() == "n":
    quit()

LINES = """rm -rf data
mkdir data"""

for i in LINES.split("\n"):
    os.system(i)
