from time import sleep
import azure.storage.blob as azureblob
import os
from datetime import datetime, timedelta

from webdriver_util import init
from processing import prep_doc
from page_scraping import login, acquire_report
from azure_util import upload_file_to_container

def get_process_post_data(date = None):
    # Check date argument
    if date == None:
        # get the date 2 days ago (safest refresh time)
        date = datetime.today() - timedelta(days=2)

    # Open AMR and download
    print("Getting ARM page...")
    driver.get(AMR_address)
    sleep(5)
    print("Downloading ARM data...")
    blob_path = acquire_report(driver, date)
    file_path = datapath + '/AMRDataExport.xls'
    if os.path.isfile(file_path):
        print("Uploading raw file to Azure...")
        blob_name = '/'.join([blob_path, 'raw/AMRDataExport.xls'])
        upload_file_to_container(blob_client, container_name, blob_name, file_path)
        print("Processing raw file...")
        processed_path = prep_doc(file_path)
        print("Uploadling processed file to Azure...")
        blob_name = '/'.join([blob_path, 'processed/AMRDataExport.csv'])
        upload_file_to_container(blob_client, container_name, blob_name, processed_path)
    else:
        print('No data available for that date...')

    # Open HDD
    print("Getting HDD page...")
    driver.get(HDD_address)
    sleep(5)
    print("Downloading HDD data...")
    blob_path = acquire_report(driver, date)
    file_path = datapath + '/HHDataExport.xls'
    if os.path.isfile(file_path):
        print("Uploading raw file to Azure...")
        blob_name = '/'.join([blob_path, 'raw/HHDataExport.xls'])
        upload_file_to_container(blob_client, container_name, blob_name, file_path)
        print("Processing raw file...")
        processed_path = prep_doc(file_path)
        print("Uploadling processed file to Azure...")
        blob_name = '/'.join([blob_path, 'processed/HHDataExport.csv'])
        upload_file_to_container(blob_client, container_name, blob_name, processed_path)
    else:
        print('No data available for that date...')

    print("Done!")

import argparse

parser = argparse.ArgumentParser(description='Retrieve BMS data for a given set of dates.')
parser.add_argument('--start_date',
                   help='A date string in the following format dd/mm/yyy')
parser.add_argument('--end_date',
                   help='A date string in the following format dd/mm/yyy')
args = parser.parse_args()

# Web Scraping configuration
login_address = 'https://ssebusiness.co.uk/Restricted/MyAccount/'
AMR_address = 'https://ssebusiness.co.uk/Restricted/MyAccount/Reporting/HHDataExtractAmr.aspx'
HDD_address = 'https://ssebusiness.co.uk/Restricted/MyAccount/Reporting/HHDataExtract.aspx'

uname = 'burohappoldcvd'
pword = 'Sunshine17'

# Azure Blob Storage Configuration
accountname = 'bhenergydatastore'
accountkey = 'nLZvyCTJXknUWeCeZSG2vOPA7uix4cpjLd4YIoPzTJTIwBoCUl6xIINTZySD6uSoTfoB2xiOW6wAP4qsiurm1w=='

container_name = 'burohappoldukmeters'

blob_client = azureblob.BlockBlobService(account_name=accountname, account_key=accountkey)

print("Loading Firefox driver...")
driver, waiter, selector, datapath = init()

# Open page and login
print("Getting login page...")
driver.get(login_address)
sleep(5)
print("Logging in...")
login(driver, uname, pword)

if args.start_date and args.end_date:
    start_date = datetime.strptime(agrs.start_date, '%d/%m/%Y')
    end_date = datetime.strptime(args.end_date, '%d/%m/%Y')
    day = timedelta(days=1)

    while start_date <= end_date:
        get_process_post_data(start_date)
        start_date = start_date + day
else:
    get_process_post_data()
