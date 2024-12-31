import os
import shutil
import sys
import time
from instabot import Bot

# Redirect stderr to null to hide error messages
sys.stderr = open(os.devnull, "w")

# Prompt the user for login credentials
username = input("Enter your Instagram username: ")
password = input("Enter your Instagram password: ")
print("\nPlease wait. This should only take a few moments...\n\n-")
# Define the session directory
session_dir = "instabot_session10192019200"

# Clean up the session directory if it already exists
if os.path.exists(session_dir):
    shutil.rmtree(session_dir, ignore_errors=True)

# Recreate the session directory
os.makedirs(session_dir, exist_ok=True)

# Initialize the bot
bot = Bot(base_path=session_dir)

# Login
bot.login(username=username, password=password)

# Get followers and followings
followers = set(bot.get_user_followers(username))
followings = set(bot.get_user_following(username))

# Find who doesn't follow you back
not_following_back = followings - followers

# Print results
print("Users who don't follow you back:")
for user_id in not_following_back:
    print(bot.get_username_from_user_id(user_id))

# Logout
bot.logout()

# Ensure all log handlers are closed to release file locks
for handler in bot.logger.handlers:
    handler.close()
    bot.logger.removeHandler(handler)

# Retry removing the session directory with error handling
for attempt in range(3):
    try:
        shutil.rmtree(session_dir)
        print("Session directory cleaned up successfully.")
        break
    except PermissionError as e:
        print(f"Attempt {attempt + 1} to remove session directory failed.")
        time.sleep(2)
else:
    print("Failed to remove session directory after multiple attempts.")

# Restore stderr after script execution
sys.stderr = sys.__stderr__