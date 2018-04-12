from azure_utilities import upload_file_to_container, send_to_sql

def clean_document(in_path, out_path):
    print('Reading from ' + in_path)
    doc = open(in_path)
    soup = BeautifulSoup(doc.read())
    doc.close()
    rows = soup.find_all('tr')

    headers = list()

    for item in rows[1].find_all('td')[:3]:
        headers.append(item.contents[0])

    for item in rows[0].find_all('td')[3:]:
        headers.append(item.contents[0])

    df_prep = list()

    for row in rows[2:]:
        tmp_list = list()
        for item in row.find_all('td'):
            tmp_list.append(item.contents[0])
        df_prep.append(tmp_list)

    df = pd.DataFrame(df_prep, columns=headers)

    ids = df.columns[:3].tolist()
    values = df.columns[3:].tolist()
    df_new = pd.melt(df,
                     id_vars=ids,
                     var_name = 'Time',
                     value_vars=values,
                     value_name='Consumption')

    # Date Time creation and type manipulation
    df_new['DateTime'] = df_new['Date'] + ' ' + df_new['Time']
    df_new['DateTime'] = pd.to_datetime(df_new['DateTime'], format='%d/%m/%Y %H:%M')

    # Consumption column to numeric
    df_new['Consumption'] = pd.to_numeric(df_new['Consumption'])


    df_new = df_new.set_index(pd.DatetimeIndex(df_new['DateTime']))

    df_new = df_new.drop(['Date', 'Time', 'DateTime'], axis=1)
    df_new['COREMPAN'] = pd.to_numeric(df_new['COREMPAN'])

    df_new.to_csv(out_path, float_format='%.2f')

    return df_new

def process_and_push_document(blob_path, filename, blob_client, container_name, \
                              file_path, cursor, cnxn):
    print("Uploading raw file to Azure...")
    blob_name = '/'.join([blob_path, 'raw', filename])
    upload_file_to_container(blob_client, container_name, blob_name, file_path)
    print("Processing raw file...")
    out_path = re.sub('xls', 'csv',file_path)
    df = prep_doc(file_path, out_path)
    print('Uploading processed data to SQL database...')
    send_to_sql(df, cursor, cnxn)
    print("Uploadling processed file to Azure...")
    blob_name = '/'.join([blob_path, 'processed/AMRDataExport.csv'])
    upload_file_to_container(blob_client, container_name, blob_name, processed_path)

    print("Cleaning up downloaded and processed files...")
    os.remove(file_path)
    os.remove(out_path)
