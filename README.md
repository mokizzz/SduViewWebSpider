# README

信息检索课程设计[sdu视点新闻](http://view.sdu.edu.cn/)全站爬虫爬取+索引构建+搜索引擎查询练习程序（1805）。

|Author|爱吃大板|
|---|---
|E-mail|rayiooo@foxmail.com

>爬虫功能使用Python的scrapy库实现，并用MongoDB数据库进行存储。
>
>索引构建和搜索功能用Python的Whoosh和jieba库实现。（由于lucene是java库，所以pyLucene库的安装极其麻烦，因此选用Python原生库Whoosh实现，并使用jieba进行中文分词。）
>
>搜索网页界面用django实现，页面模板套用[BootCDN](http://www.bootcdn.cn/)。


## 要求
以下是检索的基本要求：可以利用lucene、nutch等开源工具，利用Python、Java等编程语言，但需要分别演示并说明原理。
* 1. __Web网页信息抽取__
以山东大学新闻网为起点进行网页的循环爬取，保持爬虫在view.sdu.edu.cn之内（即只爬取这个站点的网页），爬取的网页数量越多越好。

* 2. __索引构建__
对上一步爬取到的网页进行结构化预处理，包括基于模板的信息抽取、分字段解析、分词、构建索引等。

* 3. __检索排序__
对上一步构建的索引库进行查询，对于给定的查询，给出检索结果，明白排序的原理及方法。

## 运行方式
* 运行 sduspider/run.py 来进行网络爬虫，这个过程将持续十多个小时，但可以随时终止，在下次运行时继续。

* 运行 indexbuilder/index_builder.py 来对数据库中的72000条数据构建索引，该过程将持续几个小时，但可以随时终止。

* 如果不熟悉Whoosh库的构建索引和query搜索功能，可以参考运行 indexbuilder/sample.py 。

* 运行 indexbuilder/query.py （取消最后两行注释）来测试搜索功能。

* 运行 searchengine/run_server.py 打开搜索网页服务器，在浏览器中打开[127.0.0.1:8000](127.0.0.1:8000)进入搜索页面执行搜索。

## 所需python库
* scrapy
* requests
* pymongo
* whoosh
* jieba
* django

## 所需数据库
* MongoDB
* Mongo Management Studio 可视化工具（可选）

## 爬虫特性
### (1)宽度优先搜索爬取
爬虫基于宽度优先搜索，对[http://www.view.sdu.edu.cn/](http://www.view.sdu.edu.cn/)区段的网址进行爬取，并将[http://www.view.sdu.edu.cn/info/](http://www.view.sdu.edu.cn/info/)区段的新闻内容提取出来。
### (2)二分法去重
所有已经爬取过的网址都会以MD5特征的形式顺序存储在list中，当获取新的url时，通过二分法查找list中是否存在该url的特征值，以达到去重的目的。

Scrapy库自带了查重去重的功能，但为了保证效率，自行编写了二分法去重，但并未关闭scrapy库自带的去重功能。
### (3)断点续爬
每爬取一定次数后都会将当前爬虫状态存储在pause文件夹下，重新运行爬虫时会继续上一次保存的断点进行爬取。Scrapy有自带的断点续爬功能（在settings.py中设置），但貌似在Pycharm中行不通。

### (4)数据存入MongoDB
关系类数据库不适用于爬虫数据存储，因此使用非关系类数据库MongoDB。数据库可以用可视化工具方便查看，例如Mongo Management Studio。

![Mongo Management Studio 可视化工具显示.jpg](https://i.loli.net/2018/05/24/5b065b225414c.jpg)

## 索引构建特性
### (1)断点续构
构建倒排索引的过程比较缓慢，每小时只能构建10000条新闻的索引，因此在索引构建时及时存储新构建的索引，以保证能够断点续构。

### (2)中文分词
Whoosh自带的Analyzer分词仅针对英文文章，而不适用于中文。从jieba库中引用的ChineseAnalyzer保证了能够对Documents进行中文分词。同样，ChineseAnalyzer在search时也能够对中文查询query提取关键字并进行搜索。

## 搜索引擎特性
### (1)Django搭建Web界面
Django适合Web快速开发。result页面继承了main页面，搜索结果可以按照result中的指示显示在页面中。在django模板继承下，改变main.html中的页面布局，result.html的布局也会相应改变而不必使用Ctrl+c、Ctrl+v的方式改变。

![姜海涛的搜索结果.jpg](https://i.loli.net/2018/05/24/5b0662e1a68f5.jpg)

### (2)搜索迅速
第一次搜索时，可能因为倒排索引index的取出时间较长而搜索缓慢，但一旦index取出，对于70000余条新闻的搜索将非常迅速，秒出结果。

## 参考资料
[scrapy爬虫框架入门实例](https://blog.csdn.net/zjiang1994/article/details/52779537)

[笔记：scrapy爬取的数据存入MySQL，MongoDB](https://blog.csdn.net/wqh_jingsong/article/details/54981344)

[搜索那些事 - 用Golang写一个搜索引擎(0x00) --- 从零开始（分享自知乎网）](https://zhuanlan.zhihu.com/p/20938685?utm_source=qq&utm_medium=social&utm_member=MWIxZDY0Nzg4YWQ5ODRkYzhlNzAyMDZiMTgwZTE0NzM%3D%0A)

[Whoosh + jieba 中文检索](https://www.jianshu.com/p/127c8c0b908a)

[利用whoosh对mongoDB的中文文档建立全文检索](https://www.cnblogs.com/Micang/p/6346437.html)

[Django 创建第一个项目](http://www.runoob.com/django/django-first-app.html)

[Django模板系统(非常详细)](https://blog.csdn.net/zhangxinrun/article/details/8095118/)
