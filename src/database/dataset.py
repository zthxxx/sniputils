import dataset


def connection_url(config):
    drive = config.get('drive', 'mysql+pymysql')
    connect = config['connection']
    url = f'{drive}://{connect["user"]}:{connect["passwd"]}@' \
          f'{connect["host"]}:{connect["port"]}/{connect["database"]}?charset=utf8'
    return url


def create_session(config):
    """
    create dataset session to sql database

    :param config: connection config dict
    :type config: dict

    .. code:: python

        {
            'drive': 'mysql+pymysql',
            'connection': {
                'host': 'xxx',
                'port': 3306,
                'database': 'database name',
                'user': 'username',
                'passwd': 'password'
            }
        }

    :return: database session
    """
    session = dataset.connect(connection_url(config),
                              engine_kwargs={'pool_recycle': 7200})
    return session
