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

    print('Uploading file {} to container [{}]...'.format(blob_name,
                                                          container_name))

    file_path = os.path.abspath(file_path)
    block_blob_client.create_container(container_name, fail_on_exist=False)
    block_blob_client.create_blob_from_path(container_name,
                                            blob_name,
                                            file_path)

    return 'File succesfully uploaded!'

def send_to_sql(df, cursor, cnxn):
    data = []

    for row in df.iterrows():
        dt = row[1][0]
        meter = row[1][1]
        reading_type = row[1][2]
        consumption = row[1][3]

        datum = (dt, meter, reading_type, consumption)
        data.append(datum)

    cursor.executemany("insert into dbo.meter_data(DateTime, meter_id, Reading_Type, Consumption) values (?, ?, ?, ?)", data)
    cnxn.commit()
