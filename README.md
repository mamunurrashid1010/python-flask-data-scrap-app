# Data Scraping Flask API

This project is a Flask-based API for scraping auction data from the [Commonwealth Auctions](https://www.commonwealthauctions.com/all-auctions) website and saving it into a CSV file. The API also includes functionality to clear previously scraped files from the public directory.

## Features

- Scrapes auction data from the Commonwealth Auctions website.
- Saves the scraped data into a CSV file.
- Deletes all files in the `public` directory before scraping new data.
- Lightweight API with two endpoints:
    - `/` (Home)
    - `/api/get-data` (Scrape and save auction data)

---

## Requirements

- Python 3.7 or later
- Flask
- Selenium
- BeautifulSoup4
- Chrome WebDriver

### Python Packages
- `flask`
- `selenium`
- `beautifulsoup4`
- `chromedriver-autoinstaller` (optional, for easier WebDriver setup)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
#### On Windows:
```bash
venv\Scripts\activate
```
#### On Mac/Linux:
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install flask selenium beautifulsoup4 chromedriver-autoinstaller
```

---

## Run the Application

1. Ensure the Chrome browser is installed on your system.
2. Start the Flask app:
   ```bash
   python app.py
   ```
3. The app will be accessible at `http://localhost:5000`.

---

## API Endpoints

### 1. Home Endpoint
**URL:** `/`

**Method:** `GET`

**Description:** Returns a welcome message.

**Example Response:**
```text
Welcome to the data scraping Flask API
```

### 2. Data Scraping Endpoint
**URL:** `/api/get-data`

**Method:** `GET`

**Description:** Deletes existing files in the `public` directory, scrapes auction data from Commonwealth Auctions, and saves it to a CSV file.

**Example Response:**
```json
{
  "delete_message": "All files in ./public have been deleted.",
  "scrape_message": "Data saved to ./public/commonwealthauctions.com.csv"
}
```

---

## Directory Structure
```
project-directory/
  |-- app.py                # Main application file
  |-- venv/                 # Virtual environment directory
  |-- public/               # Directory for storing CSV files
  |-- requirements.txt      # (Optional) Dependency list
```

---

## Notes

- **Headless Chrome**: The application uses Chrome in headless mode for scraping. Ensure `chromedriver` matches your Chrome version.
- **Error Handling**: Basic error handling is implemented for missing directories and failed deletions.
- **Execution Policy on Windows**: If you encounter errors activating the virtual environment, update the execution policy:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- **Sleep Time**: Adjust the `time.sleep(5)` in the scraping function if the page load time is insufficient.

---

## Future Enhancements

- Implement better error handling and logging.
- Convert the project into a Dockerized application.
- Use `WebDriverWait` instead of `time.sleep` for dynamic content loading.

---

## License

This project is licensed under the [MIT License](LICENSE).
