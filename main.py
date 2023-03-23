# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from fpdf import FPDF
import json

def create_api_doc(collection):
    for item in collection['item']:
        # Create a PDF document for each API endpoint
        # Set up the PDF document
        pdf = FPDF()
        pdf.add_page()
        pdf.set_title(item['name'])

        # Add a section for each piece of information
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"API URL: {item['request']['url']['raw']}", ln=1)
        pdf.cell(0, 10, f"API method: {item['request']['method']}", ln=1)
        pdf.cell(0, 10, f"API payload: ", ln=1)
        if item.get('response', None):
            data_json = json.dumps(item['request']['body'], indent=4)
            # Remove newline characters from JSON string
            data_json = data_json.replace('\\n', '')
            data_json = data_json.replace('\\r', '')

            # Write JSON string to PDF
            pdf.set_font('Courier', '', 10)
            pdf.multi_cell(0, 6, data_json)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"API response: ", ln=1)
        if item.get('response', None):
            data_json = json.dumps(item['response'][0]['body'], indent=4)
            # Remove newline characters from JSON string
            data_json = data_json.replace('\\n', '')
            data_json = data_json.replace('\\', '')

            # Write JSON string to PDF
            pdf.set_font('Courier', '', 10)
            pdf.multi_cell(0, 6, data_json)

        # Save the PDF document with the name of the API endpoint
        pdf.output(f"{item['name']}.pdf")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import requests

    # Replace 'your_postman_api_key' with your actual Postman API key
    api_key = 'PMAK-641bf48a4d0713691ab030d3-fe31638c51aebf57d549454dd2bcb66055'

    # Replace 'your_collection_name' with the name of the collection you want to fetch APIs for
    collection_name_to_fetch = 'University Rewamp'

    url = 'https://api.getpostman.com/collections'

    headers = {
        'X-Api-Key': api_key,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        collections = response.json()['collections']

        # Find the collection with the specified name
        collection = next((c for c in collections if c['name'] == collection_name_to_fetch), None)

        if collection:
            collection_id = collection['uid']
            collection_url = f"https://api.getpostman.com/collections/{collection_id}"
            collection_response = requests.get(collection_url, headers=headers)

            if collection_response.status_code == 200:
                detailed_collection = collection_response.json()['collection']
                print(f"APIs in the '{collection_name_to_fetch}' collection:")

                for item in detailed_collection['item']:
                    create_api_doc(item)



            else:
                print(
                    f"Error fetching collection '{collection_name_to_fetch}'. Status code: {collection_response.status_code}")

        else:
            print(f"Collection with name '{collection_name_to_fetch}' not found.")
    else:
        print(f"An error occurred while fetching API collections. Status code: {response.status_code}")






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
