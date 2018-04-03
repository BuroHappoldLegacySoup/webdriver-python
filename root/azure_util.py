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
