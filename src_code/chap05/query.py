#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from py2neo import Graph, Node, Relationship, NodeMatcher


def query(query_SQL):
    '''
    查询Neo4j数据库
    :param query_SQL: 查询命令
    :return:
    '''
    # 连接数据库
    graph = Graph("http://localhost:11010", username="neo4j", password="123456")
    # 存储查询结果
    result = []
    # 执行查询语句
    query_result = graph.run(query_SQL)
    for i in query_result:
        result.append(i.items()[0][1])
    return result


if __name__ == '__main__':
    # 查询电影《英雄》的电影简介信息
    query_SQL = "match (m:Movie)-[]->() where m.title='英雄' return m.introduction"
    result = query(query_SQL)
    print('query result:', result)
