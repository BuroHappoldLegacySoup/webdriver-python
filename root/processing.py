from bs4 import BeautifulSoup
import pandas as pd

def prep_doc(path):
    print('Reading from ' + path)
    doc = open(path)
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

    df_new = df_new.drop(['Date', 'Time'], axis=1)

    # Save to processed folder
    split_path = path.split('/')
    filename = split_path[2].split('.')[0] + '.csv'
    processed_path = '/'.join(['/usr/scripts/processed',filename])

    df_new.to_csv(processed_path)

    return processed_path
