from whoosh.index import open_dir
# from whoosh.query import *
from whoosh.qparser import QueryParser, MultifieldParser


class Query:
    def __init__(self):
        self.ix = open_dir('index')
        self.searcher = self.ix.searcher()

    def search(self, parameter):
        # 从parameter中取出要执行搜索的字段（如newsContent, newsUrl）
        parser = None
        list = parameter['keys']
        if len(list) == 1:
            parser = QueryParser(list[0], schema=self.ix.schema)
        if len(list) > 1:
            parser = MultifieldParser(list, schema=self.ix.schema)

        # 执行搜索
        myquery = parser.parse(parameter['keywords'])
        results = self.searcher.search(myquery)
        print(len(results))
        for i in range(1, len(results)):
            print(results[i - 1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.searcher.close()
        print('Query close.')

q = Query()
parameter = {
    'keys': ['newsTitle', 'newsContent'],
    'keywords': '马克思学院'
}
q.search(parameter)
