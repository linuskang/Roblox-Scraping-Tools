import requests
import time

def check_account(user_id, headers):
    url = f"https://users.roblox.com/v1/users/{user_id}"

    # Retry logic for 429 error with a countdown
    while True:
        response = requests.get(url, headers=headers)

        # Check if the response is valid and the user data contains 'isBanned'
        if response.status_code == 200:
            data = response.json()
            is_banned = data.get('isBanned', False)  # Default to False if not found

            if is_banned:
                print(f"❌ User ID: {user_id} - Banned")
            else:
                print(f"✅ User ID: {user_id} - Active")
            return
        elif response.status_code == 404:
            print(f"❌ User ID: {user_id} - Deactivated")
            return
        elif response.status_code == 429:
            # Countdown for 60 seconds
            for i in range(60, 0, -1):
                print(f"⚠️ Too many requests! Waiting {i} seconds before retrying...")
                time.sleep(1)  # Wait for 1 second each loop
            print(f"✅ Retrying after 60 seconds...")
        else:
            print(f"⚠️ User ID: {user_id} - Error {response.status_code}")
            return

def check_specific_user():
    user_id = input("Enter the user ID: ")
    headers = {
        'User-Agent': 'Roblox-Account-Checker/1.0'
    }

    check_account(user_id, headers)

if __name__ == "__main__":
    check_specific_user()
