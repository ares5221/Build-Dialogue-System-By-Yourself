#-*- coding: UTF-8 -*-

# !!!注意需要先启动Neo4j，Douban-Movie-Database数据库start

from py2neo import Graph,Node,Relationship,NodeMatcher

class Query():
    def __init__(self):
        self.graph=Graph("http://localhost:11010", username="neo4j",password="123456")

    # 问题类型0，查询电影得分
    def run(self,cql):
        # find_rela  = test_graph.run("match (n:Person{name:'张学友'})-[actedin]-(m:Movie) return m.title")
        result=[]
        find_rela = self.graph.run(cql)
        for i in find_rela:
            result.append(i.items()[0][1])
        return result




if __name__ == '__main__':
    SQL=Query()
    result=SQL.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.introduction")
    print(result)