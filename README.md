# README
信息检索课程设计sdu视点新闻全站爬取（[view.sdu.edu.cn]）练习程序（1805），使用Python的Scrapy库进行实现。

|Author|爱吃大板|
|---|---
|E-mail|rayiooo@foxmail.com
# 要求
以下是检索的基本要求：可以利用lucene、nutch等开源工具，利用Python、Java等编程语言，但需要分别演示并说明原理。
* 1. Web网页信息抽取
以山东大学新闻网为起点进行网页的循环爬取，保持爬虫在view.sdu.edu.cn之内(即只爬取这个站点的网页)，爬取的网页数量越多越好。

* 2. 索引构建
对上一步爬取到的网页进行结构化预处理，包括基于模板的信息抽取、分字段解析、分词、构建索引等。

* 3. 检索排序
对上一步构建的索引库进行查询，对于给定的查询，给出检索结果，明白排序的原理及方法。
# 运行方式
运行 sduspider/run.py.
# 所需python库
* scrapy
* requests
* pymongo
# 所需数据库
* MongoDB
* Mongo Management Studio 可视化工具（可选）
# 爬虫特性
## (1)二分法去重
所有已经爬取过的网址都会以MD5特征的形式顺序存储在list中，当获取新的url时，通过二分法查找list中是否存在该url的特征值，以达到去重的目的。
Scrapy库自带了查重去重的功能，但为了保证效率，自行编写了二分法去重，但并未关闭scrapy库自带的去重功能。
## (2)断点续爬
每隔一段时间都会将当前爬虫状态存储在pause文件夹下，重新运行爬虫时会继续上一次保存的断点进行爬取。Scrapy有自带的断点续爬功能（在settings.py中设置），但貌似在Pycharm中行不通。
# 参考资料
[scrapy爬虫框架入门实例](https://blog.csdn.net/zjiang1994/article/details/52779537)

[笔记：scrapy爬取的数据存入MySQL，MongoDB](https://blog.csdn.net/wqh_jingsong/article/details/54981344)

[搜索那些事 - 用Golang写一个搜索引擎(0x00) --- 从零开始（分享自知乎网）](https://zhuanlan.zhihu.com/p/20938685?utm_source=qq&utm_medium=social&utm_member=MWIxZDY0Nzg4YWQ5ODRkYzhlNzAyMDZiMTgwZTE0NzM%3D%0A)

