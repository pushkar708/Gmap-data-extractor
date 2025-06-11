# 📍 Google Maps Business Data Scraper

This Python script scrapes business details from Google Maps based on search terms provided in `.txt` files located in the same directory. It extracts information such as business name, address, website, reviews, phone number, and URL for each business. The collected data is then saved into both Excel and JSON files.

> **Note:** Scraping Google Maps may be against Google’s Terms of Service. Use this tool responsibly and consider alternative, approved APIs (such as the Google Places API) for production or commercial use.

---

## 📚 Features

- **Input Handling:** Reads search texts from all `.txt` files in the current working directory.
- **Automated Browser Interaction:** Utilizes Selenium in headless mode to interact with Google Maps.
- **Dynamic Scrolling:** Automatically scrolls through the feed until the end of the list is reached.
- **Detailed Data Extraction:** Gathers key business details including:
  - Business Name
  - Address
  - Website (Text & URL)
  - Average Reviews
  - Review Count
  - Phone Number
  - Google Maps URL
- **Data Export:** Saves results as:
  - An Excel file using `xlsxwriter`
  - A JSON file
- **Randomization:** Introduces randomized delays and a fixed user-agent to mimic human behavior.

---

## ⚙️ Requirements

### Python Libraries

Install the required libraries using pip:

```bash
pip install selenium xlsxwriter
```

> **Additional Libraries:**  
> - Standard libraries such as `os`, `time`, `json`, and `random` are used.
> - Make sure your Python environment is properly set up.

### Browser & WebDriver

- **Google Chrome** (latest version recommended)
- **ChromeDriver:** Ensure ChromeDriver is installed and available on your system PATH. Download [ChromeDriver](https://sites.google.com/chromium.org/driver/).

---

## 🚀 Getting Started

1. **Clone or Download the Repository:**  
   Ensure the `main.py` file is in your working directory.

2. **Prepare Your Search Files:**  
   Place one or more `.txt` files in the same directory, each containing a search term that will be used on Google Maps.

3. **Run the Script:**

   ```bash
   python main.py
   ```

4. **Process:**  
   - The script reads each `.txt` file and submits the contained search text.
   - It navigates through the Google Maps results, scrolls until the end, and collects business details.
   - For each search term, it generates an Excel file and a JSON file with business data.
   - The filename includes the number of records found and a safe version of the search text (spaces replaced with underscores).

5. **Output Files:**  
   Files are saved in the current working directory with names such as:

   - `10_My_Search_Term.xlsx`
   - `10_My_Search_Term.json`

---

## 🔧 Customization

- **User-Agent & Headless Mode:**  
  The browser is launched in headless mode and uses a fixed user-agent. To adjust these:
  ```python
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--headless=new")
  chrome_options.add_argument("--user-agent=Your_Custom_User_Agent")
  ```
  You can also randomize or change these as needed.

- **Scrolling & Delays:**  
  The script uses `time.sleep()` with random uniform delays to simulate human behavior. Adjust these values if necessary to optimize scraping speed versus reliability.

- **XPath Locators:**  
  XPaths are used to locate elements on the Google Maps page. If Google updates their page structure, you may need to update these locators.

- **File Naming:**  
  To ensure safe file names, you might consider additional sanitation of `text_to_search`.

---

## ⚠️ Disclaimer & Security Considerations

- **Terms of Service:**  
  Google Maps scraping is potentially against Google’s Terms of Service. This script should be used only for educational and personal purposes. For commercial use, consider using the official APIs with proper authentication.

- **Sensitive Information:**  
  No personal credentials or sensitive information are exposed in this script. However, be cautious when deploying or sharing the script as it interacts with external web services.

- **Error Handling:**  
  While the script includes basic error handling with delays and checks to ensure element visibility, further improvements can be made to robustly handle cases where elements are not found or when timeouts occur.

---

## 🛠️ Code Overview

- **get_file_text():**  
  Reads and concatenates the content of all `.txt` files in the current directory.

- **Browser Initialization:**  
  Configures Chrome in headless mode with custom options and opens [Google Maps](https://www.google.com/maps).

- **Search & Scrolling:**  
  For each search term, the script:
  - Clicks the search box
  - Submits the query via simulated keyboard events
  - Scrolls the results feed until the end is reached

- **Data Extraction:**  
  Each business’s details are scraped from its Google Maps page by navigating to the business URL.

- **Data Export:**  
  Extracted data is saved both in an Excel file (using `xlsxwriter`) and in a JSON file.

---

## 📃 License

This project is open-source and available under the **MIT License**.

---

## 👨‍💻 Author

**Wolfie Crypto**  
Built with dedication and care to automate business data collection from Google Maps.

---

If you have any questions or suggestions for improvements, please feel free to open an issue or submit a pull request. Enjoy and use responsibly!
