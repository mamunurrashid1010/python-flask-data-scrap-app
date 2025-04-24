# Flask Data Scraping API

This project is a **Flask-based API** for scraping auction data from websites and sending the extracted data as CSV files to a specified API endpoint. It uses **Selenium** for web scraping and **BeautifulSoup** for parsing HTML.

## Features
- Web scraping auction data from:
  - https://www.commonwealthauctions.com/all-auctions
  - https://www.re-auctions.com/Auction-Schedule
  - https://sullivan-auctioneers.com/calendar/
  - https://auctionsnewengland.com/Auctions.php
  - https://patriotauctioneers.com/auction-results/
  - https://apg-online.com/auction-schedule/
  - https://www.harmonlawoffices.com/auctions
  - https://www.baystateauction.com/auctions/state/ma
  - https://www.harkinsrealestate.com/auction-schedule/
  - https://paulmcinnis.com/auctions/all-auctions
  - http://auctionsri.com/scripts/auctions.asp?category=R
  - https://www.amgauction.com/auctions
- Saves scraped data as CSV files.
- Sends the CSV files to an external API.
- Automatically deletes old files before generating new data.
- Scheduled scraping every 2 hours using **APScheduler**.

## Prerequisites
- Python 3.7+
- ChromeDriver (compatible with your installed Chrome version)

## Dependencies
The project uses the following Python packages:
- `Flask`: Web framework for building the API.
- `selenium`: Used to control the Chrome WebDriver.
- `beautifulsoup4`: For parsing HTML content.
- `apscheduler`: For scheduling periodic tasks.
- `requests`: To send files to an external API.
- `csv`: For working with CSV files.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mamunurrashid1010/python-flask-data-scrap-app.git
   cd python-flask-data-scrap-app
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download and set up ChromeDriver:
  - Ensure `chromedriver` is in your system `PATH`.
  - Alternatively, specify its path in your script if necessary.

## Usage
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. The API will be available at `http://0.0.0.0:5000/`.

### Endpoints
- `GET /`
  - Returns a welcome message.
- `GET /api/get-data`
  - Scrapes all data from the auction websites, saves them to CSV files, and sends them to the specified API endpoint.
- `GET /api/site/<site_name>/get-data`
    - Scrapes data from the auction websites (website wise), saves them to CSV files, and sends them to the specified API endpoint.

## Functions
Scrapes data from multiple sites and saves it to a CSV file.

### `delete_public_directory_files(directory_path)`
Deletes all files in the specified public directory.

### `schedule_get_data()`
Runs the `get_data()` function within Flask's app context.

### `send_csv_file(api_url, output_file_path)`
Send the generated CSV file to the provided API endpoint (function implementation required).

## Scheduler
The script uses **APScheduler** to run the scraping process every 2 hours automatically:
```python
scheduler.add_job(schedule_get_data, 'interval', hours=2)
```

## Deployment
To run the Flask server in production, consider using **Gunicorn** or **uWSGI**:
```bash
pip install gunicorn
```
Run with:
```bash
gunicorn -w 4 app:app
```

## Notes
- Ensure `chromedriver` is compatible with the version of Chrome installed on your machine.
- Adjust `time.sleep(5)` or use `WebDriverWait` for better handling of dynamic content.
- Ensure proper error handling and logging for production use.

## License
This project is licensed under the MIT License.


