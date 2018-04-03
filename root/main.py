from webdriver_util import init
from time import sleep
import azure.storage.blob as azureblob
import os

def query_google(keywords):
    print("Loading Firefox driver...")
    driver, waiter, selector, datapath = init()

    print("Fetching google front page...")
    driver.get("http://google.com")

    print("Taking a screenshot...")
    waiter.shoot("frontpage")

    print("Typing query string...")
    selector.get_and_clear("input[type=text]").send_keys(keywords)

    print("Hitting Enter...")
    selector.get("input[type=submit]").click()

    print("Waiting for results to come back...")
    waiter.until_display("#ires")

    print
    print("The top search result is:")
    print
    print('    "{}"'.format(selector.get("#ires a").text))
    print

def login(browser, uname, pword):
    username = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_UserName"]')
    password = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_Password"]')

    username.send_keys(uname)
    password.send_keys(pword)

    login = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_LoginButton"]')

    login.click()

def acquire_report(browser, start_date=None):
    from datetime import datetime, timedelta

    if start_date != None:
        # get the date 2 days ago (safest refresh time)
        start_date = datetime.today() - timedelta(days=2)

    day = start_date.strftime('%d')
    month = start_date.strftime('%m')
    year = start_date.strftime('%Y')

    start_day = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startDay"]/option[text()={}]'.format(day)).click()
    end_day = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endDay"]/option[text()={}]'.format(day)).click()

    start_Month = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startMonth"]/option[text()={}]'.format(month)).click()
    end_Month = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endMonth"]/option[text()={}]'.format(month)).click()

    start_Year = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startYear"]/option[text()={}]'.format(year)).click()
    end_Year = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endYear"]/option[text()={}]'.format(year)).click()

    select_all = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_chkSelectAll"]').click()
    excel_export = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_reportType_1"]').click()

    EXPORT = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_btnGenerateReport"]').click()

    return start_date.strftime('%Y/%m/%d')

def upload_file_to_container(block_blob_client, container_name, blob_name, file_path):
    """
    Uploads a local file to an Azure Blob storage container.
    :param block_blob_client: A blob service client.
    :type block_blob_client: `azure.storage.blob.BlockBlobService`
    :param str container_name: The name of the Azure Blob storage container.
    :param str file_path: The local path to the file.
    :rtype: `azure.batch.models.ResourceFile`
    :return: A ResourceFile initialized with a SAS URL appropriate for Batch
    tasks.
    """

    import datetime
    import azure.storage.blob as azureblob

    print('Uploading file {} to container [{}]...'.format(blob_name,
                                                          container_name))

    file_path = os.path.abspath(file_path)
    block_blob_client.create_container(container_name, fail_on_exist=False)
    block_blob_client.create_blob_from_path(container_name,
                                            blob_name,
                                            file_path)

    sas_token = block_blob_client.generate_blob_shared_access_signature(
        container_name,
        blob_name,
        permission=azureblob.BlobPermissions.READ,
        expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=24))

    sas_url = block_blob_client.make_blob_url(container_name,
                                              blob_name,
                                              sas_token=sas_token)

    return 'File succesfully uploaded!'

if __name__ == '__main__':
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

    # Open AMR and download
    print("Getting ARM page...")
    driver.get(AMR_address)
    sleep(5)
    print("Downloading ARM data...")
    blob_path = acquire_report(browser)
    file_path = 'usr/scripts/root/ski_data_download/AMRDataExport.xls'
    blob_name = '/'.join([blob_path, 'AMRDataExport.xls'])
    upload_file_to_container(blob_client, container_name, blob_name, file_path)

    # Open HDD
    print("Getting HDD page...")
    driver.get(HDD_address)
    sleep(5)
    print("Downloading HDD data...")
    blob_path = acquire_report(driver)
    file_path = 'usr/scripts/root/ski_data_download/HHDataExport.xls'
    blob_name = '/'.join([blob_path, 'HHDataExport.xls'])
    upload_file_to_container(blob_client, container_name, blob_name, file_path)
    print("Done!")
