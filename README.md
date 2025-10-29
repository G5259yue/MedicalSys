
# 改版

# 部署

```bash
#Neo4j linux
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/neotechnology.gpg
echo 'deb [signed-by=/etc/apt/keyrings/neotechnology.gpg] https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update

apt install neo4j
#windows
https://neo4j.ac.cn/deployment-center/
```

# todo

那个index.vue的图没调正我整不好ai也搞不定，后面再弄