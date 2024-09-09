from kfp.dsl import component


@component(
    base_image          = 'registry.access.redhat.com/ubi9/python-311:latest',
    packages_to_install = [
        'elasticsearch',
        'langchain',
        'langchain-community',
        'langchain-elasticsearch',
        'pypdf',
        'tensorflow',
        'tensorflow-hub',
        'tensorflow-text'
    ]
)
def index_document(
    elasticsearch_host                 : str,
    elasticsearch_username             : str,
    elasticsearch_password             : str,
    elasticsearch_document_index       : str,
    tensorflow_hub_embedding_model_url : str,
    pvc_file                           : str
) -> None:

    from elasticsearch                        import Elasticsearch
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.embeddings       import TensorflowHubEmbeddings
    from langchain_community.vectorstores     import ElasticsearchStore

    pdf_loader = PyPDFLoader(
        file_path = pvc_file
    )

    documents = pdf_loader.load_and_split()

    elasticsearch_client = Elasticsearch(
        hosts        = elasticsearch_host,
        basic_auth   = (elasticsearch_username, elasticsearch_password),
        verify_certs = False
    )

    embedding = TensorflowHubEmbeddings(
        model_url = tensorflow_hub_embedding_model_url
    )

    elasticsearch_store = ElasticsearchStore(
        es_connection = elasticsearch_client,
        index_name    = elasticsearch_document_index,
        embedding     = embedding
    )

    for document in documents:

        elasticsearch_store.add_documents(
            documents = [document]
        )

    elasticsearch_store.client.indices.refresh(
        index = elasticsearch_document_index
    )
