from flask import Flask,request,jsonify
from py2neo import Graph
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# 连接到Neo4j数据库
url = "bolt://localhost:7687"
username = "neo4j"
password = "20060917"
graph = Graph(url, auth=(username, password))


Max_num=200  #可视化界面生成最多的节点数
depth=3      #递归深度
def non_recursive_query(source, n, links):
    stack = [(source, n)]
    visited = set()  # 记录已经访问过的节点

    while stack:
        current_node, depth = stack.pop()

        # 如果当前节点已经访问过或者达到了指定的深度，直接跳过
        if current_node in visited or depth <= 0:
            continue

        # 执行查询
        query = f"""
            MATCH (n {{name: '{current_node}'}})-[r]->(m)
            RETURN n.name AS source, type(r) AS rela, m.name AS target
        """
        result = graph.run(query)
        # 将当前节点标记为已访问
        visited.add(current_node)

        for record in result:
            if len(links) >= Max_num:
                break  # 达到最大节点数，跳出循环
            target = record["target"]
            links.append({
                "source": current_node,
                "rela": record["rela"],
                "target": target
            })
            stack.append((target, depth - 1))

    return links

@app.route('/api/view')
def api_view():
    search_term = request.args.get('search_term', '')
    links = []
    non_recursive_query(search_term, 3, links)
    return jsonify(links)

if __name__ == '__main__':
    # test = []
    # non_recursive_query("晕厥",3,test)
    # print(test)
    app.run(debug=True, host='0.0.0.0', port=5000)