import requests
import csv
import time
import webbrowser
from urllib.parse import urlparse, parse_qs

def get_authorization_url(client_id):
    base_url = "https://trakt.tv/oauth/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    }
    auth_url = f"{base_url}?{'&'.join([f'{key}={val}' for key, val in params.items()])}"
    return auth_url

def get_access_token(client_id, client_secret, auth_code):
    token_url = "https://api.trakt.tv/oauth/token"
    payload = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, json=payload)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    else:
        raise Exception("Error obtaining access token")

def add_movies_to_list(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": YOUR_CLIENT_ID,
    }

    base_url = "https://api.trakt.tv"
    add_to_list_url = f"{base_url}/sync/watchlist"

    def add_movie(title, year):
        max_retries = 5
        retries = 0

        while retries < max_retries:
            payload = {
                "movies": [
                    {
                        "title": title,
                        "year": year,
                    }
                ]
            }

            response = requests.post(add_to_list_url, headers=headers, json=payload)

            if response.status_code == 201:
                print(f"Movie '{title}' added to the Trakt list.")
                break
            elif response.status_code == 429:
                # Retry if the rate limit is exceeded (status code 429)
                print(f"Rate limit exceeded. Retrying in 5 seconds... (Retry {retries + 1}/{max_retries})")
                time.sleep(5)
                retries += 1
            else:
                print(response.status_code)
                print(f"Error adding movie '{title}' to the Trakt list, skipping.")
                break

    with open("watchlist.csv", 'r') as csvfile:
        letterboxd_data = csv.reader(csvfile, delimiter=',')
        next(letterboxd_data)
        for row in letterboxd_data:
            if any(field.strip() for field in row):  # Check if any field in the row contains data
                title, year = row[1], row[2]
                add_movie(title, year)
                time.sleep(0.8)
            else:
                break  # Stop the loop when encountering an empty row

if __name__ == "__main__":
    YOUR_CLIENT_ID = ""
    YOUR_CLIENT_SECRET = ""

    auth_url = get_authorization_url(YOUR_CLIENT_ID)
    print("Open the following URL in your web browser, if it doesn't open automatically:")
    print(auth_url)

    # Open the URL in the web browser for the user to grant permission
    webbrowser.open_new_tab(auth_url)

    # Ask the user to input the authorization code
    auth_code = input("Enter the authorization code from the URL: ")

    access_token = get_access_token(YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, auth_code)
    add_movies_to_list(access_token)
