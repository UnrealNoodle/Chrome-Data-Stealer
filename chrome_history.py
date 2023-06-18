import sqlite3
import shutil
import os

# Get the username of the PC
username = os.environ["USERNAME"]

# Path to the Google Chrome history database file
original_db = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default/History"
copy_db = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default/HistoryCopy"

# Create a copy of the History file
shutil.copyfile(original_db, copy_db)

# Connect to the copied database
conn = sqlite3.connect(copy_db)
cursor = conn.cursor()

# Execute a query to fetch browsing history
cursor.execute("SELECT url, title FROM urls")

# Fetch all rows returned by the query
rows = cursor.fetchall()

# Create the file path for the output file in the temporary directory
temp_dir = os.environ["TEMP"]
output_file = os.path.join(temp_dir, "Chrome History.txt")

# Open the file in write mode
with open(output_file, "w", encoding="utf-8") as file:
    # Write the browsing history to the file
    for row in rows:
        url = row[0]
        title = row[1]
        file.write(f"URL: {url}\n")
        file.write(f"Title: {title}\n")
        file.write("--------------------\n")

# Close the database connection
conn.close()