from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

# whoosh+jieba 初步学习样例

cnAnalyzer = ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True, analyzer=cnAnalyzer), content=TEXT(stored=False, analyzer=cnAnalyzer), path=ID(stored=True))

import os.path
if not os.path.exists('sample_index'):
    os.mkdir('sample_index')
ix = create_in('sample_index', schema)
ix = open_dir('sample_index')

writer = ix.writer()
writer.add_document(title=u'爱吃大板的博客', content=u'大家好！这里是爱吃大板的博客，欢迎光临！大板是一种雪糕。')
writer.add_document(title=u'蝴蝶定理吃雪糕', content=u'好阿婆雪糕蝴蝶定理最爱吃了！必须买下来。It\'s tasty!')
writer.commit()
writer = ix.writer()
writer.add_document(title=u"My document", content=u"This is my document!")
writer.add_document(title=u"Second try", content=u"This is the second example.", path='http://sdu.edu.cn/')
writer.add_document(title=u"Third time's the charm", content=u"Examples are many.", path='http://sdu.edu.cn/')
writer.commit()

try:
    searcher = ix.searcher()
    # myquery = And([Term('content', u'second'), Term('content', u'example')])
    parser = QueryParser('content', ix.schema)
    myquery = parser.parse(u'雪糕')
    results = searcher.search(myquery)
    print(len(results))
    print(results[0])
finally:
    searcher.close()