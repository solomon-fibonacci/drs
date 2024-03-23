import logging
import os

from apis.datastore.service.interface import Datastore
from apis.datastore.service.mongo import MongoDBDatastore
from apis.datastore.service.disk import OnDiskDatastore

logger = logging.getLogger(__name__)


def get_datastore() -> Datastore:
    """
    Returns an implemenation of the Datastore interface depending on the app environment settings
    """
    mongo_uri = os.environ.get("MONGO_URI", None)
    mongo_dbname = os.environ.get("MONGO_DBNAME", None)
    mongo_cert_file = os.environ.get("MONGO_DB_CERT_FILE", None)
    if mongo_uri and mongo_dbname:
        logger.info("Using MongoDB datastore")
        datastore = MongoDBDatastore(mongo_uri,
                                     mongo_dbname,
                                     cert_file=mongo_cert_file)
    else:
        datastore = OnDiskDatastore()
        logger.info("Using on-disk datastore")

    return datastore
