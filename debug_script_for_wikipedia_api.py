import requests

def fetch_html_section(title, section):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'parse',
        'page': title,
        'section': section,
        'prop': 'text',
        'format': 'json'
    }
    response = requests.get(url, params=params)
    print("Raw response content:", response.content)  # Print raw response content for debugging
    try:
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()  # Attempt to parse JSON
        return data['parse']['text']['*']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")
        print("Response content:", response.content)
    return None

page_title = '2024_Summer_Olympics_medal_table'
section_index = 2  # Adjust based on the section containing the table

# Fetch HTML content of the section
html_content = fetch_html_section(page_title, section_index)
print(html_content)  # Print the fetched HTML content
