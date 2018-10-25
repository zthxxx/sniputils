import json

from bson import json_util
import oss2

from ..snippets import classproperty


class Bucket(object):
    path_delimiter = '/'
    headers = {'x-oss-server-side-encryption': 'AES256'}
    _bucket = None
    _oss_config = None

    def __init__(self, oss_config):
        """
        :param oss_config: dict
        {
            'key_id': '', 'secret': '',
            'host': '', 'bucket': '',
        }
        """
        if isinstance(oss_config, oss2.Bucket):
            self.overwrite_bucket(oss_config)
        self.set_oss_config(oss_config)

    @classmethod
    def set_oss_config(cls, oss_config: dict):
        assert 'key_id' in oss_config
        assert 'secret' in oss_config
        assert 'host' in oss_config
        assert 'bucket' in oss_config
        cls._oss_config = oss_config

    @classmethod
    def overwrite_bucket(cls, bucket):
        assert isinstance(bucket, oss2.Bucket)
        cls._bucket = bucket

    @classmethod
    def get_bucket(cls) -> oss2.Bucket:
        auth = oss2.Auth(cls._oss_config['key_id'], cls._oss_config['secret'])
        bucket = oss2.Bucket(auth, cls._oss_config['host'], cls._oss_config['bucket'])
        return bucket

    @classproperty
    @classmethod
    def bucket(cls) -> oss2.Bucket:
        if cls._bucket is None:
            cls._bucket = cls.get_bucket()
        return cls._bucket

    @classmethod
    def get(cls, oss_path):
        return cls.bucket.get_object(oss_path)

    @classmethod
    def put(cls, oss_path, data):
        cls.bucket.put_object(
            oss_path,
            data,
            headers=cls.headers
        )

    @classmethod
    def get_json(cls, oss_path) -> dict:
        return json.loads(
            bytes.decode(cls.get(oss_path).read())
        )

    @classmethod
    def put_json(cls, oss_path, data):
        cls.put(oss_path, json.dumps(data, default=json_util.default))

    @classmethod
    def is_exists(cls, oss_path) -> bool:
        return cls.bucket.object_exists(oss_path)

    @classmethod
    def list(cls, oss_folder, **kwargs):
        return cls.bucket.list_objects(
            oss_folder,
            delimiter=cls.path_delimiter,
            **kwargs
        ).object_list
