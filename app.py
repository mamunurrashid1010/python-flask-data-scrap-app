from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import os
import time

app = Flask(__name__)

# API endpoint to home
@app.route('/')
def index():
    return "Welcom to the data scrapping flask api";

# Flask route to get scrap data
@app.route('/api/get-data', methods=['GET'])
def get_data():
    public_directory_path = './public'

    # get data from commonwealthauctions
    url = 'https://www.commonwealthauctions.com/all-auctions'
    output_file_path = os.path.join(public_directory_path, 'commonwealthauctions.com.csv')
    # Delete files in public directory
    delete_message = delete_public_directory_files(public_directory_path)
    # Scrape data
    scrape_message = commonwealthauctions_scrape_data(url, output_file_path)

    return jsonify({
        "delete_message": delete_message,
        "scrape_message": scrape_message
    })

# commonwealthauctions function
def commonwealthauctions_scrape_data(url, output_file_path):
    # Set up the Chrome WebDriver with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless mode)
    chrome_options.add_argument("--no-sandbox")  # Recommended for environments like EC2
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    driver = webdriver.Chrome(options=chrome_options)  # Ensure the ChromeDriver is installed and in your PATH
    driver.get(url)

    # Wait for the content to load (adjust the sleep time as needed or use WebDriverWait)
    import time
    time.sleep(5)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Locate the table
    table = soup.find('table', {'id': 'ma_auctions'})
    if not table:
        print("Table not found on the page.")
        driver.quit()
        return

    # Use static headers
    headers = ['date', 'address', 'state', 'status', 'deposit', 'moreinfo']

    # Extract rows
    rows = []
    tbody = table.find('tbody')
    if tbody:
        row_elements = tbody.find_all('tr')
    else:
        print("No table rows found.")
        driver.quit()
        return

    for tr in row_elements:
        cells = []
        for td in tr.find_all('td'):
            link = td.find('a')
            if link:
                cells.append(link['href'])
            else:
                cells.append(td.text.strip())
        rows.append(cells)

    # Ensure the public directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Save data to CSV
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(headers)
        writer.writerows(rows)

    print(f"Data saved to {output_file_path}")
    driver.quit()
    return f"Data saved to {output_file_path}"

# Function to delete files
def delete_public_directory_files(directory_path):
    if not os.path.exists(directory_path):
        return f"Directory {directory_path} does not exist."

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                continue
        except Exception as e:
            return f"Error deleting file {file_path}: {e}"
    return f"All files in {directory_path} have been deleted."



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
