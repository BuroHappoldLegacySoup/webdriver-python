from processing import process_and_push_document

# Web Scraping configuration
login_address = 'https://ssebusiness.co.uk/Restricted/MyAccount/'
AMR_address = 'https://ssebusiness.co.uk/Restricted/MyAccount/Reporting/HHDataExtractAmr.aspx'
HDD_address = 'https://ssebusiness.co.uk/Restricted/MyAccount/Reporting/HHDataExtract.aspx'

uname = os.getenv('SSE_USERNAME')
pword = os.getenv('SSE_PASSWORD')

# Azure Blob Storage Configuration
accountname = os.getenv('AZURE_BLOB_ACCOUNT_NAME')
accountkey = os.getenv('AZURE_BLOB_ACCOUNT_KEY')

container_name = os.getenv('AZURE_BLOB_CONTAINER_NAME')

blob_client = azureblob.BlockBlobService(account_name=accountname, account_key=accountkey)

#  Configure SQL connection
import pyodbc

server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')

driver= '{ODBC Driver 13 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Open browser
browser = webdriver.Chrome()

# Open page and login
print("Getting login page...")
browser.get(login_address)
sleep(5)
print("Logging in...")
login(browser, uname, pword)

start_date = datetime.strptime(os.getenv('START_DATE'), '%d/%m/%Y')
end_date = datetime.strptime(os.getenv('END_DATE'), '%d/%m/%Y')
day = timedelta(days=1)

if start_date != None and end_date != None:
    while start_date <= end_date:
        get_process_post_data(browser, cursor, cnxn, start_date)
        start_date = start_date + day
else:
    process_and_push_document(blob_path, filename, blob_client, container_name, \
                                  file_path, cursor, cnxn)

# Clean up database after data append
cursor.execute("select distinct * into #tmp From dbo.meter_data delete from dbo.meter_data insert into dbo.meter_data select * from #tmp drop table #tmp select * from dbo.meter_data")
cnxn.commit()
