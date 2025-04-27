import requests
import datetime
import os
import time
import concurrent.futures

def check_account(user_entry, headers):
    user_id, username = user_entry.split(" - ", 1)
    user_id = user_id.strip()

    url = f"https://users.roblox.com/v1/users/{user_id}"

    # Retry logic for 429 error with a countdown
    while True:
        response = requests.get(url, headers=headers)

        # Check if the response is valid and the user data contains 'isBanned'
        if response.status_code == 200:
            data = response.json()
            is_banned = data.get('isBanned', False)  # Default to False if not found

            if is_banned:
                return f"❌ {username} (ID: {user_id}) - Banned"
            else:
                return f"✅ {username} (ID: {user_id}) - Active"
        elif response.status_code == 404:
            return f"❌ {username} (ID: {user_id}) - Deactivated"
        elif response.status_code == 429:
            # Countdown for 60 seconds
            for i in range(60, 0, -1):
                print(f"⚠️ Too many requests! Waiting {i} seconds before retrying...")
                time.sleep(1)  # Wait for 1 second each loop
            print(f"✅ Retrying after 60 seconds...")
        else:
            return f"⚠️ {username} (ID: {user_id}) - Error {response.status_code}"

def check_accounts(filename):
    headers = {
        'User-Agent': 'Roblox-Account-Checker/1.0'
    }

    print(f"\n📂 Opening file: {filename}\n")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            users = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found.")
        return

    if not users:
        print(f"❌ File '{filename}' is empty.")
        return

    # Prepare output file for deactivated accounts
    base_filename = os.path.splitext(filename)[0]
    aest_time = datetime.datetime.utcnow() + datetime.timedelta(hours=10)  # AEST timezone
    timestamp = aest_time.strftime("%Y-%m-%d_%H-%M-%S")
    deactivated_filename = f"deactivated-{base_filename}-{timestamp}.txt"

    deactivated_users = []

    print(f"🔎 Starting to check {len(users)} users...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Use the executor to run multiple checks concurrently
        results = executor.map(lambda user_entry: check_account(user_entry, headers), users)

        # Collect results and handle deactivated users
        for result in results:
            print(result)
            if "Deactivated" in result or "Banned" in result:
                # Append both ID and username to the deactivated list
                deactivated_users.append(result.split(" - ")[0].strip())

    # Save deactivated accounts to file
    if deactivated_users:
        with open(deactivated_filename, "w", encoding="utf-8") as f:
            for user in deactivated_users:
                f.write(user + "\n")
        print(f"\n📄 Saved {len(deactivated_users)} deactivated accounts to '{deactivated_filename}'.")
    else:
        print("\n✅ No deactivated accounts found.")

    print("\n✅ Finished checking all users.\n")

if __name__ == "__main__":
    filename = input("Enter the filename to check: ")
    check_accounts(filename)
