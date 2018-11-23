from typing import Iterable, Union

from mongoengine.connection import connect, get_db
from mongoengine.base import BaseDocument


def mongo_connect(host: Union[str, list], database: str, user: str = None, passwd: str = None, **kwargs):
    """
    mongoengine global connection

    :param host: ``hostname:port`` or ``mongodb://host:port,host:port`` or ``[host, host]``
    :param database: database name
    :param user: user name
    :param passwd: password
    :param kwargs: some options in this:

    .. code:: python

        {
            'replicaSet', 'read_preference',
            'authentication_source', 'authentication_mechanism'
        }

    :return: connection
    """
    if not isinstance(host, str) and isinstance(host, Iterable):
        host = f"mongodb://{','.join(host)}"
    alias = f'{database}-{user}'
    connect(host=host, db=database, alias=alias, username=user, password=passwd, **kwargs)
    return get_db(alias)


def doc2dict(doc: Union[list, BaseDocument]):
    """
    transform mongoengine Document to python native dict

    :param doc: Document object
    :return: dict for Document data
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
