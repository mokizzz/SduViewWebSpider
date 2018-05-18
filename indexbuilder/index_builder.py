from whoosh.fields import *
from whoosh.index import *
# from whoosh.query import *
# from whoosh.qparser import *
from jieba.analyse import ChineseAnalyzer
import pymongo
from pymongo.collection import Collection
import settings


class IndexBuilder:
    def __init__(self):
        self.mongoClient = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        # self.db = self.mongoClient[settings.MONGODB_DBNAME][settings.MONGODB_SHEETNAME]
        self.db = pymongo.database.Database(self.mongoClient, settings.MONGODB_DBNAME)
        self.pagesCollection = Collection(self.db, settings.MONGODB_SHEETNAME)

    def build_index(self):
        analyzer = ChineseAnalyzer()

        # 创建索引模板
        schema = Schema(
            newsId=ID(stored=True),
            newsTitle=TEXT(stored=True, analyzer=analyzer),
            newsUrl=ID(stored=True),
            newsClick=NUMERIC(stored=True, sortable=True),
            newsPublishTime=TEXT(stored=True),
            newsContent=TEXT(stored=False, analyzer=analyzer),  # 文章内容太长了，不存
        )

        # 索引文件相关
        import os.path
        if not os.path.exists('index'):
            os.mkdir('index')
            ix = create_in('index', schema)
            print('未发现索引文件,已构建.')
        else:
            ix = open_dir('index')
            print('发现索引文件并载入....')

        # 索引构建
        writer = ix.writer()
        indexed_amount = 0
        total_amount = self.pagesCollection.find().count()
        print(total_amount)
        while True:
            try:
                row = self.pagesCollection.find_one({'indexed': 'False'})
                if row is None:
                    # all indexed is 'True' 所有条目已经处理
                    writer.commit()
                    print('所有条目索引处理完毕.')
                    break
                else:
                    # get new row 获取了新的条目

                    writer.add_document(
                        newsId=str(row['_id']),
                        newsTitle=row['newsTitle'],
                        newsUrl=row['newsUrl'],
                        newsClick=int(row['newsClick']),
                        newsPublishTime=row['newsPublishTime'],
                        newsContent=row['newsContent'],
                    )

                    # the end
                    self.pagesCollection.update_one({'_id': row['_id']}, {'$set': {'indexed': 'True'}})
                    writer.commit()     # 每次构建提交一次
                    writer = ix.writer()    # 然后重新打开
                    indexed_amount += 1
                    print(indexed_amount, '/', total_amount)
            except:
                print(row['_id'], '异常.')
                print('已处理', indexed_amount, '/', total_amount, '项.')
                break



# --------此段代码用以在数据库中缺少indexed列时补充插入indexed--------
# host = settings.MONGODB_HOST
# port = settings.MONGODB_PORT
# dbname = settings.MONGODB_DBNAME
# sheetname = settings.MONGODB_SHEETNAME
# client = pymongo.MongoClient(host=host, port=port)
# mydb = client[dbname]
# post = mydb[sheetname]
# post.update({}, {'$set':{'indexed':'False'}}, upsert=False, multi=True)   # 增加indexed项并初始化为False
# post.update({'indexed': 'True'}, {'$set':{'indexed':'False'}})
# ----------------------------------------------------------------


id = IndexBuilder()
id.build_index()
