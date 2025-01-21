from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import csv
import os
import time
import requests

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
    delete_public_directory_files(public_directory_path)
    commonwealthauctions_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from re-aution
    url = 'https://www.re-auctions.com/Auction-Schedule'
    output_file_path = os.path.join(public_directory_path, 'reauctions.csv')
    delete_public_directory_files(public_directory_path)
    re_auctions_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)


    # get data from sullivan auctioneers
    url = 'https://sullivan-auctioneers.com/calendar/'
    output_file_path = os.path.join(public_directory_path, 'sullivan_auctioneers.csv')
    delete_public_directory_files(public_directory_path)
    sullivan_auctioneers_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from auctionsnewengland
    url = 'https://auctionsnewengland.com/Auctions.php'
    output_file_path = os.path.join(public_directory_path, 'auctionsnewengland.csv')
    delete_public_directory_files(public_directory_path)
    auctionsnewengland_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from patriotauctioneers
    url = 'https://patriotauctioneers.com/auction-results/'
    output_file_path = os.path.join(public_directory_path, 'patriotauctioneers.csv')
    delete_public_directory_files(public_directory_path)
    patriot_auctioneers_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from apgonline
    url = 'https://apg-online.com/auction-schedule/'
    output_file_path = os.path.join(public_directory_path, 'apgonline.csv')
    delete_public_directory_files(public_directory_path)
    apg_online_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from harmonlawoffices
    url = 'https://www.harmonlawoffices.com/auctions'
    output_file_path = os.path.join(public_directory_path, 'harmonlawoffices.csv')
    delete_public_directory_files(public_directory_path)
    harmonlaw_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from baystateauction
    url = 'https://www.baystateauction.com/auctions/state/ma'
    output_file_path = os.path.join(public_directory_path, 'baystateauction.csv')
    delete_public_directory_files(public_directory_path)
    baystateauction_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from harkinsrealestate
    url = 'https://www.harkinsrealestate.com/auction-schedule/'
    output_file_path = os.path.join(public_directory_path, 'harkinsrealestate.csv')
    delete_public_directory_files(public_directory_path)
    harkinsrealestate_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)

    # get data from paulmcinnis
    url = 'https://paulmcinnis.com/auctions/all-auctions'
    output_file_path = os.path.join(public_directory_path, 'paulmcinnis.csv')
    delete_public_directory_files(public_directory_path)
    paulmcinnis_scrape_data(url, output_file_path)
    api_url = "https://bostonauction.iconicsolutionsbd.com/api/file/upload"
    if os.path.isfile(output_file_path):
        send_csv_file(api_url, output_file_path)


    print ("done")
    return jsonify({
        "message": "success",
    })

# send data to the endpoint- https://bostonauction.iconicsolutionsbd.com/api/file/upload
def send_csv_file(api_url, file_path):
    if not os.path.exists(file_path):
        return f"File {file_path} does not exist."

    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(api_url, files=files)
            if response.status_code == 200:
                return f"File sent successfully: {response.json()}"
            else:
                return f"Failed to send file. Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error sending file: {str(e)}"


# commonwealthauctions function
def commonwealthauctions_scrape_data(url, output_file_path):
    # Set up the Chrome WebDriver with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless mode)
    chrome_options.add_argument("--no-sandbox")  # Recommended for environments like EC2
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    try:
        driver = webdriver.Chrome(options=chrome_options)  # Ensure ChromeDriver is installed and in your PATH
        driver.get(url)

        # Wait for the content to load (adjust the sleep time as needed or use WebDriverWait)
        time.sleep(5)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate the table
        table = soup.find('table', {'id': 'ma_auctions'})
        if not table:
            driver.quit()
            return "Table not found on the page."

        # Use static headers
        headers = ['date', 'address', 'state', 'status', 'deposit', 'moreinfo']

        # Extract rows
        rows = []
        tbody = table.find('tbody')
        if tbody:
            row_elements = tbody.find_all('tr')
        else:
            driver.quit()
            return "No table rows found."

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

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


def re_auctions_scrape_data(url, output_file_path):
    # Set up the Chrome WebDriver with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless mode)
    chrome_options.add_argument("--no-sandbox")  # Recommended for environments like EC2
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    try:
        driver = webdriver.Chrome(options=chrome_options)  # Ensure ChromeDriver is installed and in your PATH
        driver.get(url)

        # Wait for the content to load (adjust the sleep time as needed or use WebDriverWait)
        time.sleep(5)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate the auction listings
        rows = soup.find_all('div', class_='row rowspacer')
        if not rows:
            driver.quit()
            return "No auction listings found on the page."

        # Prepare headers for the CSV
        headers = ['auction_url', 'property_address', 'property_type', 'auction_status', 'deposit_amount', 'postponed_date', 'auction_title', 'auction_date_time']

        # Extract auction details from the page
        data = []
        for row in rows:
            # Extract the title (text of the auction link)
            auction_url = row.find('a', {'class': 'listingtitle'})['href'] if row.find('a', {'class': 'listingtitle'}) else None
            property_address = row.find('a', {'class': 'listingtitle'}).text.strip() if row.find('a', {'class': 'listingtitle'}) else None
            property_type = row.find('li', text=lambda x: x and 'Property Type:' in x).text.replace('Property Type:', '').strip() if row.find('li', text=lambda x: x and 'Property Type:' in x) else None
            # auction_status = row.find('li', text=lambda x: x and 'Auction Status:' in x).find('b').text.strip() if row.find('li', text=lambda x: x and 'Auction Status:' in x) else None
            status_element = row.find('li', text=lambda x: x and 'Auction Status:' in x)
            if status_element:
                # Use find instead of text filter to handle nested tags
                auction_status = status_element.get_text(strip=True).replace('Auction Status:', '').strip()
            else:
                auction_status = None
            deposit_amount = row.find('li', text=lambda x: x and 'Deposit Amount:' in x).text.replace('Deposit Amount:', '').strip() if row.find('li', text=lambda x: x and 'Deposit Amount:' in x) else None
#             auction_date = row.find('b').text.strip() if row.find('b') else None
            postponed_date = row.find('div', class_='Postponed').text.strip() if row.find('div', class_='Postponed') else None

            # Extract the auction date and time
            auction_date_time = row.find('div', class_='col-xs-12 col-sm-3 col-md-3 col-lg-3').find('b').text.strip() if row.find('div', class_='col-xs-12 col-sm-3 col-md-3 col-lg-3') and row.find('div', class_='col-xs-12 col-sm-3 col-md-3 col-lg-3').find('b') else None

            # Extract the auction title (link text)
            auction_title = row.find('a', {'class': 'listingtitle'}).text.strip() if row.find('a', {'class': 'listingtitle'}) else None

            # Append the extracted data for this auction
            data.append([auction_url, property_address, property_type, auction_status, deposit_amount, postponed_date, auction_title, auction_date_time])

        # Ensure the public directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Save data to CSV
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"



# sullivan auctioneers function
def sullivan_auctioneers_scrape_data(url, output_file_path):
    # Set up the Chrome WebDriver with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for the content to load (adjust the sleep time as needed or use WebDriverWait)
        time.sleep(5)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate the auction table
        table = soup.find('table', class_='table table-striped')
        if not table:
            driver.quit()
            return "Auction table not found on the page."

        # Use static headers for the CSV
        headers = ['date_time', 'status', 'street', 'city_state', 'description']

        # Extract rows
        data = []
        tbody = table.find('tbody')
        if tbody:
            row_elements = tbody.find_all('tr')
        else:
            driver.quit()
            return "No table rows found."

        for tr in row_elements:
            date_time = tr.find('td').find('a').text.strip() if tr.find('td').find('a') else None
            status_td = tr.find_all('td')[1] if len(tr.find_all('td')) > 1 else None
            status = status_td.find('span').text.strip() if status_td and status_td.find('span') else status_td.text.strip() if status_td else None
            street = tr.find_all('td')[2].text.strip() if len(tr.find_all('td')) > 2 else None
            city_state = tr.find_all('td')[3].text.strip() if len(tr.find_all('td')) > 3 else None
            description = tr.find_all('td')[4].text.strip() if len(tr.find_all('td')) > 4 else None

            data.append([date_time, status, street, city_state, description])

        # Ensure the public directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Save data to CSV
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


# auctionsnewengland function
def auctionsnewengland_scrape_data(url, output_file_path):
    # Set up Chrome WebDriver with headless options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Allow time for the content to load
        time.sleep(5)  # Consider using WebDriverWait for better reliability

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate the auction table
        table = soup.find('table', class_='alternate_color')
        if not table:
            driver.quit()
            return "Auction table not found on the page."

        # Define CSV headers
        headers = ['auction_title', 'status', 'date_time']

        # Extract rows
        data = []
        tbody = table.find('tbody')
        if tbody:
            row_elements = tbody.find_all('tr')
        else:
            driver.quit()
            return "No table rows found."

        for tr in row_elements:
            auction_title = tr.find('td').find('a').text.strip() if tr.find('td').find('a') else None
            status_td = tr.find_all('td')[1] if len(tr.find_all('td')) > 1 else None
            status = status_td.find('font').text.strip() if status_td and status_td.find('font') else None
            date_time_td = tr.find_all('td')[2] if len(tr.find_all('td')) > 2 else None
            date_time = date_time_td.contents[0].strip() if date_time_td else None

            data.append([auction_title, status, date_time])

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Save data to CSV
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

# patriotauctioneers function
def patriot_auctioneers_scrape_data(url, output_file_path):
    # Set up the Chrome WebDriver with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for the content to load
        time.sleep(5)  # Increase if necessary

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate the auction calendar section
        calendar_section = soup.find('section', id='calendar')
        if not calendar_section:
            driver.quit()
            return "Calendar section not found on the page."

        # Use static headers for the CSV
        headers = ['property_address', 'auction_date', 'short_description', 'status']

        # Extract auction listings
        data = []
        auction_lists = calendar_section.find_all('a', class_='auction-list')

        for auction in auction_lists:
            address = auction.find('h1').text.strip() if auction.find('h1') else None
            auction_date = auction.find('div', class_='auction-date').text.strip() if auction.find('div', class_='auction-date') else None
            descriptions = auction.find_all('div', class_='auction-short-desc')
            short_description = ", ".join([desc.text.strip() for desc in descriptions]) if descriptions else None
            sale_status = auction.find('div', class_='banner').text.strip() if auction.find('div', class_='banner') else None

            data.append([address, auction_date, short_description, sale_status])

        # Ensure the public directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Save data to CSV
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

# apg_online function
def apg_online_scrape_data(url, output_file_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)  # Adjust wait time as needed

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        properties = soup.find_all('article', class_='property')

        if not properties:
            driver.quit()
            return "No properties found on the page."

        headers = ['auction_date', 'auction_status', 'address', 'description', 'required_deposit', 'more_info_link']
        data = []

        for prop in properties:
            auction_date = prop.find('dt', text='Auction Date:').find_next('dd').text.strip() if prop.find('dt', text='Auction Date:') else None
            auction_status = prop.find('dt', text='Auction Status:').find_next('dd').text.strip() if prop.find('dt', text='Auction Status:') else None
            address = prop.find('dt', text='Address:').find_next('dd').text.strip() if prop.find('dt', text='Address:') else None
            description = prop.find('dt', text='Description:').find_next('dd').text.strip() if prop.find('dt', text='Description:') else None
            required_deposit = prop.find('dt', text='Required Deposit:').find_next('dd').text.strip() if prop.find('dt', text='Required Deposit:') else None
            more_info_link = prop.find('a', class_='button')['href'] if prop.find('a', class_='button') else None

            data.append([auction_date, auction_status, address, description, required_deposit, more_info_link])

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


# harmonlaw function
def harmonlaw_scrape_data(url, output_file_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(10)  # Adjust wait time as needed

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', id='ma_auctions')

        if not table:
            driver.quit()
            return "No auction table found on the page."

        headers = ['date_time', 'address_city', 'state', 'auctioneer', 'status', 'deposit', 'more_info_link']
        data = []

        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else []

        for tr in rows:
            cells = tr.find_all('td')
            if len(cells) >= 7:
                date_time = cells[0].text.strip()
                address_city = cells[1].text.strip()
                state = cells[2].text.strip()
                auctioneer = cells[3].text.strip()
                status = cells[4].text.strip()
                deposit = cells[5].text.strip()
                more_info_link = cells[6].find('a')['href'] if cells[6].find('a') else None
                data.append([date_time, address_city, state, auctioneer, status, deposit, more_info_link])

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


# baystateauction function
def baystateauction_scrape_data(url, output_file_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(10)  # Adjust wait time as needed

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the auction table
        table = soup.find('table', {'id': 'DataTables_Table_0'})

        if not table:
            driver.quit()
            return "No auction table found on the page."

        # Define the header columns
        headers = ['date_time', 'address', 'city', 'state', 'description', 'deposit', 'status', 'more_info_link']
        data = []

        # Extract table body and rows
        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else []

        for tr in rows:
            cells = tr.find_all('td')
            if len(cells) >= 7:
                # Extract data from each row
                date_time = cells[0].text.strip()
                address = cells[1].text.strip()
                city = cells[2].text.strip()
                state = cells[3].text.strip()
                description = cells[4].text.strip()
                deposit = cells[5].text.strip()

                # Extract the status (if it exists) from the first column
                status = None
                status_span = cells[0].find('span', class_='attention')
                if status_span:
                    status = status_span.text.strip()

                more_info_link = cells[6].find('a')['href'] if cells[6].find('a') else None

                # Add row data to the list
                data.append([date_time, address, city, state, description, deposit, status, more_info_link])

        # Ensure the directory for the output file exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Write data to the CSV file
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        driver.quit()
        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


# harkinsrealestate function
def harkinsrealestate_scrape_data(url, output_file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the container for properties
        properties_container = soup.find('div', class_='columns three properties')
        if not properties_container:
            return "No properties found on the page."

        properties = properties_container.find_all('article', class_='property')
        headers = ['address', 'status', 'date', 'description', 'deposit', 'more_info_link']
        data = []

        for property_item in properties:
            # Extract address
            address = property_item.find('h3', class_='title').text.strip()

            # Extract status
            status = property_item.find('p', class_='status').text.replace('Status: ', '').strip()

            # Extract date
            date = property_item.find('p', class_='date').text.strip()

            # Extract description
            description = property_item.find('p', class_='desc').text.strip()

            # Extract deposit
            deposit = property_item.find('p', class_='deposit').text.replace('Required Deposit: ', '').strip()

            # Extract more info link
            more_info_link = property_item.find('a', class_='btn')['href']

            # Append data to list
            data.append([address, status, date, description, deposit, more_info_link])

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Write data to CSV
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


# paulmcinnis function
def paulmcinnis_scrape_data(url, output_file_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for the page to load content
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        auction_listings = soup.find_all('div', class_='stripAuctionsUpcoming auctionlisting')
        if not auction_listings:
            return "No auction listings found on the page."

        headers = ['title', 'address', 'date_time', 'more_info_link']
        data = []

        for auction in auction_listings:
            auction_inner = auction.find_all('a', class_='auction-inner')
            for item in auction_inner:
                title = item.find('h4', class_='auction-title').text.strip()
                address = item.find('p', class_='auction-address').text.strip()
                date_time = item.find('p', class_='auction-datetime').text.strip()
                more_info_link = item['href']  # Base URL might need to be added if relative link
                data.append([title, address, date_time, more_info_link])

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        return f"Data saved to {output_file_path}"

    except Exception as e:
        return f"An error occurred: {str(e)}"




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


# Schedule the get_data function
def schedule_get_data():
    with app.app_context():
        get_data()

# Set up the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(schedule_get_data, 'interval', hours=2)  # Change 'minutes=1' to 'hours=1' for hourly execution
scheduler.start()


if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

