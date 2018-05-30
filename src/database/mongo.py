from typing import Iterable

from mongoengine import connect
from mongoengine.base import BaseDocument


def mongo_connect(host, database, user=None, passwd=None, **kwargs):
    """
    mongoengine global connection
    :param host: 'hostname:port' or 'mongodb://host:port,host:port'
    :param database: database name
    :param user: user name
    :param passwd: password
    :param kwargs: {
            replicaSet, read_preference,
            authentication_source, authentication_mechanism
        }
    :return: connection
    """
    if not isinstance(host, str) and isinstance(host, Iterable):
        host = f"mongodb://{','.join(host)}"
    return connect(host=host, db=database, username=user, password=passwd, **kwargs)


def doc2dict(doc):
    """
    transform mongoengine Document to python native dict
    :param doc: Document
    :return: dict for Document
    """
    if isinstance(doc, list):
        return [doc2dict(item) for item in doc]
    if isinstance(doc, BaseDocument):
        return {
            field: doc2dict(doc[field])
            for field in doc
            if doc[field] is not None
        }
    return doc
