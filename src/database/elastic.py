from typing import Callable, Tuple

import arrow
from dateutil.tz import tzlocal
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class ESSearch(object):
    def __init__(self, hosts=None, using=None, index=None):
        config = dict(index=index)
        if hosts and not using:
            using = Elasticsearch(hosts=hosts, maxsize=25, timeout=300)
        using and config.update(using=using)
        self.searching = Search(**config)
        self.tzlocal = tzlocal()

    def time_range(self, query: Search, start, end):
        start, end = arrow.get(start).naive, arrow.get(end).naive
        start, end = start.replace(tzinfo=self.tzlocal), end.replace(tzinfo=self.tzlocal)
        return query.filter('range', **{'@timestamp': {'gte': start, 'lte': end}}).sort('-@timestamp')

    def query_string(self, query_str: str, range: Tuple[str, str] = None):
        query = self.searching.query('query_string', query=query_str)
        if range:
            query = self.time_range(query, *range)
        return query

    def query(self, query_str: str, limit: int = None, **kwargs):
        query = self.query_string(query_str, **kwargs)
        if limit is None:
            return query.scan()
        else:
            return query[:limit].execute()

    def apply_query(self, query_str: str, apply_func: Callable, is_dict=False, **kwargs):
        for item in self.query(query_str, **kwargs):
            item = item.to_dict() if is_dict else item
            yield apply_func(item)
