import requests


class Tools:
    def __init__(self):
        pass

    def get_redirected_url(url: str):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            # Send a GET request to the URL, allow redirects (default behavior)
            response = requests.get(url, allow_redirects=True, headers=headers)

            # Return the final redirected URL
            return response.url

        except requests.exceptions.RequestException as e:
            # Handle any exceptions (e.g., network issues, invalid URL)
            print(f"Error fetching the URL: {e}")
            return None
