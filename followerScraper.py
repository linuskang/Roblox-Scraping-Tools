import requests
import datetime

def fetch_username(user_id):
    """Fetch the username for a given user ID."""
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['name']
    else:
        print(f"❌ Failed to fetch username for user {user_id}: {response.status_code}")
        return None

def scrape_followers(user_id):
    # Roblox API to fetch followers
    base_url = f"https://friends.roblox.com/v1/users/{user_id}/followers?limit=100"
    headers = {'User-Agent': 'Roblox-Follower-Scraper/1.0'}

    follower_ids = []
    cursor = None
    total_scraped = 0
    page_count = 1

    # First pass: Scrape all follower IDs
    while True:
        url = base_url
        if cursor:
            url += f"&cursor={cursor}"

        print(f"[Page {page_count}] Fetching follower IDs...")

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch followers: {response.status_code}")
            break

        data = response.json()

        if not data['data']:
            print("⚠️ No more followers found.")
            break

        for entry in data['data']:
            follower_ids.append(entry['id'])
            total_scraped += 1

        cursor = data.get('nextPageCursor')
        if not cursor:
            print(f"\n✅ No more pages. Finished scraping follower IDs.\n")
            break

        print(f"[Page {page_count}] Finished scraping {total_scraped} follower IDs so far.\n")
        page_count += 1

    if not follower_ids:
        print("❌ No followers found.")
        return

    # Second pass: Fetch usernames for each follower
    followers = []
    for follower_id in follower_ids:
        username = fetch_username(follower_id)

        if username:
            followers.append(f"{follower_id} - {username}")
            print(f"  Scraped follower ID: {follower_id} - {username}")

    # Format filename with timestamp
    aest_time = datetime.datetime.utcnow() + datetime.timedelta(hours=10)  # AEST = UTC+10
    timestamp = aest_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"followers-{user_id}-{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for follower in followers:
            f.write(f"{follower}\n")

    print(f"✅ Scraped total {len(followers)} followers.")
    print(f"📄 Saved to file: {filename}\n")

if __name__ == "__main__":
    user_id = input("Enter the Roblox user ID to scrape followers: ")
    scrape_followers(user_id)
