from kfp.dsl import component


@component(
    base_image          = 'registry.access.redhat.com/ubi9/python-311:latest',
    packages_to_install = ['boto3']
)
def download_document(
    s3_service_name      : str,
    s3_endpoint_url      : str,
    s3_access_key_id     : str,
    s3_secret_access_key : str,
    s3_region            : str,
    s3_bucket            : str,
    s3_file              : str,
    pvc_directory        : str
) -> str:

    from boto3 import client
    from os    import path

    pvc_file = path.join(pvc_directory, path.basename(s3_file))

    s3_client = client(
        service_name          = s3_service_name,
        endpoint_url          = s3_endpoint_url,
        aws_access_key_id     = s3_access_key_id,
        aws_secret_access_key = s3_secret_access_key,
        region_name           = s3_region
    )

    s3_client.download_file(
        Bucket   = s3_bucket,
        Key      = s3_file,
        Filename = pvc_file
    )

    return pvc_file
