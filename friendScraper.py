import requests
import datetime
import os

def scrape_user_friends(user_id):
    friends = []
    cursor = None
    headers = {
        'User-Agent': 'Roblox-Friend-Scraper/1.0'
    }

    print(f"\nStarting to scrape friends for user ID {user_id}...\n")

    # Prepare filename immediately
    aest_time = datetime.datetime.utcnow() + datetime.timedelta(hours=10)  # AEST = UTC+10
    timestamp = aest_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scrapedFriends-{user_id}-{timestamp}.txt"

    # Create file immediately
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")  # create empty file

    try:
        url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
        print("Fetching friends list...")

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch friends: {response.status_code}")
            return

        data = response.json()
        if not data['data']:
            print("No friends found.")
            return

        with open(filename, "a", encoding="utf-8") as f:
            for friend in data['data']:
                friend_info = f"{friend['id']} - {friend['name']}"
                friends.append(friend_info)
                f.write(friend_info + "\n")
                print(f"  Scraped friend: {friend['name']} (ID: {friend['id']})")

    except KeyboardInterrupt:
        print("\n⚡ Scraping interrupted by user (CTRL+C). Saving progress...\n")

    if not friends:
        print("No friends found.")
        return

    print(f"\n✅ Scraped total {len(friends)} friends.")
    print(f"📄 Saved to file: {filename}\n")

if __name__ == "__main__":
    user_id = input("Enter the Roblox user ID: ")
    scrape_user_friends(user_id)
