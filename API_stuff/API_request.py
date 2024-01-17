import requests

def get_data_from_API(url):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extracting JSON data from the response
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: Status code {response.status_code}")
        return None

# Example usage
url = "http://example.com/api/books"
data = get_data_from_API(url)
print(data)