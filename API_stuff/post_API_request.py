import requests

def add_book_to_API(url, book_data):
    response = requests.post(url, json=book_data)

    if response.status_code == 201:  # 201 is the typical status code for a successful creation
        print("Book added successfully!")
        return response.json()  # Return the response data
    else:
        print(f"Failed to add book: Status code {response.status_code}")
        return None

# Example usage
url = "http://example.com/api/books"
new_book = {
    "title": "Example Book",
    "author": "Author Name",
    "isbn": "123-456-789"
}
result = add_book_to_API(url, new_book)
print(result)