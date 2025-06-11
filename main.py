from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import os
import time
import json
import xlsxwriter

# Get the current working directory
cwd = os.path.dirname(os.path.abspath(__file__))

def get_file_text():
    text_list=[]
    for files in os.listdir(cwd):
        if files.endswith(".txt"):
            with open(os.path.join(cwd,files), 'r') as f:
                text_list.append(f.read())
    return text_list

start_time = time.time()
chrome_options=Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
driver=webdriver.Chrome(options=chrome_options)
actions=ActionChains(driver=driver)
driver.maximize_window()
driver.get("https://www.google.com/maps")

time.sleep(random.uniform(2,3))

text_to_search_list=get_file_text()

for text_to_search in text_to_search_list:

    driver.find_elements(By.XPATH,"//input[@id='searchboxinput']")[0].click()
    actions.send_keys(text_to_search).perform()
    time.sleep(random.uniform(1,2))
    actions.send_keys(Keys.ENTER).perform()

    time.sleep(random.uniform(5,8))


    while True:
        scrollable_area = driver.find_elements(By.XPATH,"//div[@role='feed']")[0]
        if scrollable_area.is_displayed():
            break
        else:
            time.sleep(random.uniform(1,2))
            

    while True:
        end_of_list=driver.find_elements(By.XPATH,"//span[contains(text(),'the end')]")
        if len(end_of_list) != 0:
            if end_of_list[0].is_displayed():
                break
        
        driver.execute_script("arguments[0].scrollBy(0, 1000000);", scrollable_area)
        time.sleep(random.uniform(3,4.5))

    # Extract URLs of all search results
    all_results_list = driver.find_elements(By.XPATH, "//a[@class='hfpxzc']")
    all_result_urls = [item.get_attribute('href') for item in all_results_list]

    business_data = []

    # Visit each business URL and scrape details
    for url in all_result_urls:
        driver.get(url)
        time.sleep(random.uniform(2, 3))

        business_name = driver.find_elements(By.XPATH, "//div[@role='main']//h1")[0].text if driver.find_elements(By.XPATH, "//div[@role='main']//h1") else "Not Available"
        
        business_address = driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'address')]//div[contains(@class,'fontBodyMedium')]")[0].text if driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'address')]//div[contains(@class,'fontBodyMedium')]") else "Not Available"
        
        business_website_text = driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'authority')]//div[contains(@class,'fontBodyMedium')]")[0].text if driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'authority')]//div[contains(@class,'fontBodyMedium')]") else "Not Available"
        
        business_website_url = driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'authority')]")[0].get_attribute('href') if driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'authority')]") else "Not Available"
        
        business_avg_review = driver.find_elements(By.XPATH, "//div[@class='PPCwl']//div[@class='YTkVxc ikjxab']")[0].get_attribute('aria-label') if driver.find_elements(By.XPATH, "//div[@class='PPCwl']//div[@class='YTkVxc ikjxab']") else "Not Available"
        
        business_review_count = driver.find_elements(By.XPATH, "//button[contains(@class,'HHrUdb fontTitleSmall rqjGif')]//span")[0].text if driver.find_elements(By.XPATH, "//button[contains(@class,'HHrUdb fontTitleSmall rqjGif')]//span") else "Not Available"
        
        business_phone = driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'phone')]//div[contains(@class,'fontBodyMedium')]")[0].text if driver.find_elements(By.XPATH, "//*[contains(@data-item-id,'phone')]//div[contains(@class,'fontBodyMedium')]") else "Not Available"
        
        business_url = driver.current_url

        business_data.append({
            "Business Name": business_name,
            "Business Address": business_address,
            "Business Website Text": business_website_text,
            "Business Website URL": business_website_url,
            "Business Average Review": business_avg_review,
            "Business Review Count": business_review_count,
            "Business Phone": business_phone,
            "Business Url": business_url
        })

    driver.quit()

    # Save data to Excel
    workbook = xlsxwriter.Workbook(os.path.join(cwd, f'{len(business_data)}_{text_to_search.replace(" ","_")}.xlsx'))
    worksheet = workbook.add_worksheet()

    # Write headers and data to Excel
    headers = ['Business Name', 'Business Address', 'Business Website Text', 'Business Website URL', 'Business Average Review', 'Business Review Count', 'Business Phone', 'Business Url (Maps)']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, data in enumerate(business_data, start=1):
        worksheet.write(row_num, 0, data['Business Name'])
        worksheet.write(row_num, 1, data['Business Address'])
        worksheet.write(row_num, 2, data['Business Website Text'])
        worksheet.write(row_num, 3, data['Business Website URL'])
        worksheet.write(row_num, 4, data['Business Average Review'])
        worksheet.write(row_num, 5, data['Business Review Count'])
        worksheet.write(row_num, 6, data['Business Phone'])
        worksheet.write(row_num, 7, data['Business Url'])

    workbook.close()

    # Save data to JSON
    with open(os.path.join(cwd, f'{len(business_data)}_{text_to_search.replace(" ","_")}.json'), 'w') as json_file:
        json.dump(business_data, json_file, indent=4)

    end_time = time.time()

    # Print total time taken
    print(f"""Data saved to f'{len(business_data)}_{text_to_search.replace(" ","_")}.xlsx' and f'{len(business_data)}_{text_to_search.replace(" ","_")}.json'""")
    print(f"Total time taken: {time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))}")