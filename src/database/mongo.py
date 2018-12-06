from typing import Iterable, Union

from mongoengine.base import BaseDocument
from mongoengine.connection import DEFAULT_CONNECTION_NAME, connect, get_db


def mongo_connect(host: Union[str, list], database: str, user: str = None, passwd: str = None,
                  auto_alias: Union[bool, str] = False, **kwargs):
    """
    mongoengine global connection

    :param host: ``hostname:port`` or ``mongodb://host:port,host:port`` or ``[host, host]``
    :param database: database name
    :param user: user name
    :param passwd: password
    :param auto_alias: bool | str, setting a alias connection name, or auto gen
    :param kwargs: some options in this:

    .. code:: python

        {
            'replicaSet', 'read_preference',
            'authentication_source', 'authentication_mechanism'
        }

    :return: connection
    """
    alias = DEFAULT_CONNECTION_NAME
    if auto_alias:
        alias = f'{database}-{user}' if type(auto_alias) is bool else auto_alias
    if not isinstance(host, str) and isinstance(host, Iterable):
        host = f"mongodb://{','.join(host)}"
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
