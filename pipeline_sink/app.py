from flask      import Flask, request
from kfp.client import Client
from os         import getenv, path

app = Flask(__name__)

kubeflow_host   = getenv('KUBEFLOW_HOST')
kubeflow_client = Client(host = kubeflow_host)


@app.route('/index_document', methods = ['POST'])
def index_document():

    pipeline_yaml = path.join('yaml', 'index_document.yaml')

    pipeline_arguments = {
        'pvc_name'                           : getenv('PVC_NAME'),
        'pvc_storage_class'                  : getenv('PVC_STORAGE_CLASS'),
        'pvc_access_modes'                   : getenv('PVC_ACCESS_MODES').split(sep = ','),
        'pvc_size'                           : getenv('PVC_SIZE'),
        's3_service_name'                    : getenv('S3_SERVICE_NAME'),
        's3_endpoint_url'                    : getenv('S3_ENDPOINT_URL'),
        's3_access_key_id'                   : getenv('S3_ACCESS_KEY_ID'),
        's3_secret_access_key'               : getenv('S3_SECRET_ACCESS_KEY'),
        's3_region'                          : getenv('S3_REGION'),
        's3_bucket'                          : getenv('S3_BUCKET'),
        's3_file'                            : getenv('S3_FILE'),
        'elasticsearch_host'                 : getenv('ELASTICSEARCH_HOST'),
        'elasticsearch_username'             : getenv('ELASTICSEARCH_USERNAME'),
        'elasticsearch_password'             : getenv('ELASTICSEARCH_PASSWORD'),
        'elasticsearch_index'                : getenv('ELASTICSEARCH_INDEX'),
        'tensorflow_hub_embedding_model_url' : getenv('TENSORFLOW_HUB_EMBEDDING_MODEL_URL')
    }

    kubeflow_client.create_run_from_pipeline_package(
        pipeline_file = pipeline_yaml,
        arguments     = pipeline_arguments
    )
