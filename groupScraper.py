import requests
import datetime
import os
import time
import concurrent.futures

def scrape_group_members(group_id):
    members = []
    cursor = None
    headers = {
        'User-Agent': 'Roblox-Scraper/1.0'
    }

    print(f"\nStarting to scrape members from group {group_id}...\n")

    # Prepare filename first
    aest_time = datetime.datetime.utcnow() + datetime.timedelta(hours=10)  # AEST = UTC+10
    timestamp = aest_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scrapedMembers-{group_id}-{timestamp}.txt"

    # Create file immediately
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")  # just create empty file

    total_scraped = 0
    page_count = 1

    try:
        while True:
            url = f"https://groups.roblox.com/v1/groups/{group_id}/users?limit=100&sortOrder=Asc"
            if cursor:
                url += f"&cursor={cursor}"

            print(f"[Page {page_count}] Fetching members...")

            response = requests.get(url, headers=headers)

            if response.status_code == 429:
                # Retry logic for rate limit (429)
                print("⚠️ Too many requests! Waiting 60 seconds before retrying...")
                for i in range(60, 0, -1):
                    print(f"⚠️ Waiting {i} seconds before retrying...")
                    time.sleep(1)
                print(f"✅ Retrying after 60 seconds...\n")
                continue  # Retry the current page

            if response.status_code != 200:
                print(f"Failed to fetch members: {response.status_code}")
                break

            data = response.json()
            if not data['data']:
                print("No more users found on this page.")
                break

            with open(filename, "a", encoding="utf-8") as f:  # Open file once per page
                for entry in data['data']:
                    user = entry['user']
                    member_info = f"{user['userId']} - {user['username']}"
                    members.append(member_info)
                    f.write(member_info + "\n")  # Write each user immediately
                    total_scraped += 1
                    print(f"  Scraped user: {user['username']} (ID: {user['userId']})")

            cursor = data.get('nextPageCursor')
            if not cursor:
                print(f"\nNo more pages. Finished scraping.\n")
                break

            print(f"[Page {page_count}] Finished scraping {total_scraped} members so far.\n")
            page_count += 1

    except KeyboardInterrupt:
        print("\n⚡ Scraping interrupted by user (CTRL+C). Saving progress...\n")

    if not members:
        print("No members found.")
        return

    print(f"✅ Scraped total {len(members)} members.")
    print(f"📄 Saved to file: {filename}\n")

if __name__ == "__main__":
    group_id = input("Enter the Roblox group ID: ")
    scrape_group_members(group_id)
