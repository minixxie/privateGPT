import logging
import os

from injector import inject, singleton
from llama_index.storage.docstore import BaseDocumentStore, SimpleDocumentStore, MongoDocumentStore
from llama_index.storage.index_store import SimpleIndexStore, MongoIndexStore
from llama_index.storage.index_store.types import BaseIndexStore

from private_gpt.paths import local_data_path

logger = logging.getLogger(__name__)


@singleton
class NodeStoreComponent:
    index_store: BaseIndexStore
    doc_store: BaseDocumentStore

    @inject
    def __init__(self) -> None:
        if os.getenv('MONGO_URI'):
            self.index_store = MongoIndexStore.from_uri(uri=os.getenv('MONGO_URI'), db_name="private-gpt")
            self.doc_store = MongoDocumentStore.from_uri(uri=os.getenv('MONGO_URI'), db_name="private-gpt")
        else:
            try:
                self.index_store = SimpleIndexStore.from_persist_dir(
                    persist_dir=str(local_data_path)
                )
            except FileNotFoundError:
                logger.debug("Local index store not found, creating a new one")
                self.index_store = SimpleIndexStore()

            try:
                self.doc_store = SimpleDocumentStore.from_persist_dir(
                    persist_dir=str(local_data_path)
                )
            except FileNotFoundError:
                logger.debug("Local document store not found, creating a new one")
                self.doc_store = SimpleDocumentStore()
