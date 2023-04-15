from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import datetime
import pandas as pd
import json
from createSheet import createSheetFromJson
from dataProcessing import dataProcessingFromKeywords
from uploadDrive import uploadToDrive

# Config
options = Options()
options.add_argument('-headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(options=options)

wait = WebDriverWait(driver, 3)



# Url (with short data for testing ) - https://in.indeed.com/jobs?q=html%2Ccss%2Cjavascript%2Creact%2Cnode+js%2Cjava%2Cfrontend%2Cbackend&l=India&sc=0kf%3Ajt%28new_grad%29%3B&fromage=1&vjk=6b3d8cb9cdcd3ace
# url (With Long Data) = 'https://in.indeed.com/jobs?q=html%2Ccss%2Cjs%2Cjsvascript%2Creact%2Cmongo%2Cnode%2Cui%2Cweb%2Creact+js%2Cjavascript+developer%2Cmern%2Creact+developer&l=India&sc=0kf%3Ajt%28fulltime%29%3B&fromage=1&vjk=383eb1d7dee2ebc6'
url = 'https://in.indeed.com/jobs?q=html%2Ccss%2Cjavascript%2Creact%2Cnode+js%2Cjava%2Cfrontend%2Cbackend&l=India&sc=0kf%3Ajt%28new_grad%29%3B&fromage=1&vjk=6b3d8cb9cdcd3ace'
driver.get(url)

# Main Data Array
job_array = []

# For Each page
while True:

    try:
        # Wait for modal and click close button
        modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "icl-CloseButton")))
        modal.click()
    except:
        pass

    # Get Html
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    job_postings = soup.find_all('div', class_='job_seen_beacon')

    # Get data for Each page
    for job in job_postings:

        job_data = {}

        # Extract job title
        job_title_h2 = job.find('h2', class_='jobTitle')
        if job_title_h2:
            job_data['jobTitle'] = job_title_h2.a.span.text.strip()
        else:
            job_data['jobTitle'] = "NA"

        # Extract company name
        company_name_span = job.find('span', class_='companyName')
        if company_name_span:
            job_data['companyName'] = company_name_span.text.strip()
        else:
            job_data['companyName'] = "NA"

        # Extract company location
        company_location_div = job.find('div', class_='companyLocation')
        if company_location_div:
            job_data['companyLocation'] = company_location_div.text.strip()
        else:
            job_data['companyLocation'] = "NA"

        # Extract salary details
        salary_div = job.find('div', class_='salary-snippet-container')
        if salary_div:

            # "\u20b9" ->  "₹"
            string = salary_div.div.text.strip()
            salary = string.replace("\u20b9", "Rupee: ")

            job_data['salaryDetails'] = salary
        else:
            job_data['salaryDetails'] = "NA"

        # Extract job posting time
        posted_time_span = job.find('span', class_='date')
        if posted_time_span:

            # PostedJust posted -> Posted : Just posted
            s = posted_time_span.text.strip()
            fixed_part = "Posted"
            variable_part = s[len(fixed_part):].strip()
            result = f"{fixed_part} : {variable_part}"

            job_data['postedTime'] = result

        else:
            job_data['postedTime'] = "NA"

        # Extract apply link
        apply_link_a = job.find('a', class_='jcs-JobTitle')
        if apply_link_a:
            job_data['applyLink'] = 'https://in.indeed.com' + apply_link_a['href']
        else:
            job_data['applyLink'] = "NA"

        # Extract other details
        job_snippet_div = job.find('div', class_='job-snippet')
        if job_snippet_div:
            if job_snippet_div.ul:
                other_details_array = job_snippet_div.ul.find_all('li')
                if other_details_array:
                    other_details = " , ".join(
                        tag.string.strip() for tag in other_details_array if tag.string is not None)
                    job_data['otherDetails'] = other_details
                else:
                    job_data['otherDetails'] = "NA"
            else:
                job_data['otherDetails'] = "NA"
        else:
            job_data['otherDetails'] = "NA"

        # Appening all
        job_array.append(job_data)

    print("Done for a current page, Moving to next page...")
    # print(job_array)

    try:
        # Click next page button
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')))
        next_button.click()
    except:
        # End of pagination
        break

driver.quit()
print("Done All pages...")

# Sava all data into JSON Format
# Create a subdirectory named "json" if it doesn't exist
if not os.path.exists("json"):
    os.makedirs("json")

# Generating File name
today = datetime.datetime.today()
todaysDate = today.strftime('%d/%m/%Y')

# Convert date string to datetime object
date = datetime.datetime.strptime(todaysDate, '%d/%m/%Y')

# Format output string
fileName = date.strftime('%dth-%b-') + "Indeed-posts"

# Build the file paths for the JSON and Excel files
fileNameJson = os.path.join("json", fileName + ".json")

# Write the JSON data to the file
with open(fileNameJson, 'w') as f:
    json.dump(job_array, f)

# Load the JSON data into a DataFrame
with open(fileNameJson) as f:
    data = pd.read_json(f)

print("Raw Json file Created ...")

# Data Processing
dataProcessingFromKeywords()

# Create one sheet
createSheetFromJson()

# Final Processed sheet Uploaded to Drive
uploadToDrive(fileName)





