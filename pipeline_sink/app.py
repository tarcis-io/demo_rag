from flask      import Flask, request
from kfp.client import Client
from os         import getenv, path

PVC_NAME                           = getenv('PVC_NAME')
PVC_STORAGE_CLASS                  = getenv('PVC_STORAGE_CLASS')
PVC_ACCESS_MODES                   = getenv('PVC_ACCESS_MODES').split(',') if getenv('PVC_ACCESS_MODES') is not None else None
PVC_SIZE                           = getenv('PVC_SIZE')
S3_SERVICE_NAME                    = getenv('S3_SERVICE_NAME')
S3_ENDPOINT_URL                    = getenv('S3_ENDPOINT_URL')
S3_ACCESS_KEY_ID                   = getenv('S3_ACCESS_KEY_ID')
S3_SECRET_ACCESS_KEY               = getenv('S3_SECRET_ACCESS_KEY')
S3_REGION                          = getenv('S3_REGION')
S3_BUCKET                          = getenv('S3_BUCKET')
ELASTICSEARCH_HOST                 = getenv('ELASTICSEARCH_HOST')
ELASTICSEARCH_USERNAME             = getenv('ELASTICSEARCH_USERNAME')
ELASTICSEARCH_PASSWORD             = getenv('ELASTICSEARCH_PASSWORD')
ELASTICSEARCH_INDEX                = getenv('ELASTICSEARCH_INDEX')
TENSORFLOW_HUB_EMBEDDING_MODEL_URL = getenv('TENSORFLOW_HUB_EMBEDDING_MODEL_URL')

KUBEFLOW_HOST   = getenv('KUBEFLOW_HOST')
kubeflow_client = Client(host = KUBEFLOW_HOST)

app = Flask(__name__)


@app.route('/index_document', methods = ['PUT'])
def index_document():

    pipeline_yaml      = path.join('yaml', 'index_document.yaml')
    pipeline_arguments = {
        'pvc_name'                           : PVC_NAME,
        'pvc_storage_class'                  : PVC_STORAGE_CLASS,
        'pvc_access_modes'                   : PVC_ACCESS_MODES,
        'pvc_size'                           : PVC_SIZE,
        's3_service_name'                    : S3_SERVICE_NAME,
        's3_endpoint_url'                    : S3_ENDPOINT_URL,
        's3_access_key_id'                   : S3_ACCESS_KEY_ID,
        's3_secret_access_key'               : S3_SECRET_ACCESS_KEY,
        's3_region'                          : S3_REGION,
        's3_bucket'                          : S3_BUCKET,
        's3_file'                            : request.json['Key'],
        'elasticsearch_host'                 : ELASTICSEARCH_HOST,
        'elasticsearch_username'             : ELASTICSEARCH_USERNAME,
        'elasticsearch_password'             : ELASTICSEARCH_PASSWORD,
        'elasticsearch_index'                : ELASTICSEARCH_INDEX,
        'tensorflow_hub_embedding_model_url' : TENSORFLOW_HUB_EMBEDDING_MODEL_URL
    }

    kubeflow_client.create_run_from_pipeline_package(
        pipeline_file = pipeline_yaml,
        arguments     = pipeline_arguments
    )

    return f'pipeline run: { pipeline_yaml }'
