<template>
  <div class="page-container">
    <div class="shift-mode">
      <label class="search-label" for="searchID">疾病搜索词：</label>
      <input id="searchID" type="text" placeholder="例如：感冒" @keyup.enter="handleSearch" v-model="diseaseKeyword"
        class="search-input" />
      <button class="search-btn" @click="handleSearch">搜索</button>
    </div>

    <div class="map-container">
      <div class="sidebar">
        <ul class="relation-list">
          <li v-for="relation in relationList" :key="relation.value" class="relation-item"
            @click="handleRelationClick(relation.value)">
            <h2>{{ relation.label }}</h2>
            <p>{{ relation.desc }}</p>
          </li>
        </ul>
      </div>

      <div id="allmap" class="graph-container">
        <div ref="chart"></div>
        <!-- <div class="info">
          节点数量: <span>{{ nodeCount }}</span><br>
          关系边数量: <span>{{ edgeCount }}</span>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';

export default {
  name: "MedicalNeo4jGraph",
  data() {
    return {
      diseaseKeyword: "",
      relationList: [
        { value: "acompany_with", label: "伴随", desc: "会伴随节点的疾病" },
        { value: "belongs_to", label: "属于", desc: "test" },
        { value: "common_drug", label: "常用药物", desc: "test" },
        { value: "do_eat", label: "宜食", desc: "test" },
        { value: "drugs_of", label: "药物", desc: "test" },
        { value: "has_symptom", label: "有症状", desc: "test" },
        { value: "need_check", label: "需要检查", desc: "test" },
        { value: "no_eat", label: "忌食", desc: "test" },
        { value: "recommand_drug", label: "推荐药物", desc: "test" },
        { value: "recommand_eat", label: "推荐饮食", desc: "test" },
        { value: "show_all", label: "显示全部", desc: "test" }
      ],
      nodeCount: 0,
      edgeCount: 0,
      links: [], // 图谱数据
      nodes: {},
      svg: null,
      d3Elements: {},
      relationshipMap: {
        'acompany_with': '伴随',
        'belongs_to': '属于',
        'common_drug': '常用药物',
        'do_eat': '宜食',
        'drugs_of': '药物',
        'has_symptom': '有症状',
        'need_check': '需要检查',
        'no_eat': '忌食',
        'recommand_drug': '推荐药物',
        'recommand_eat': '推荐饮食'
      }
    };
  },
  mounted() {
    this.fetchGraphData();
  },
  methods: {
    async fetchGraphData() {
      // 通过后端接口获取知识图谱数据
      let search = this.diseaseKeyword.trim();
      // 上面AI写的我不知道为什么不行真傻逼 删了简化一下
      try {
        const res = await axios.get(`http://localhost:5000/api/view?search_term=${encodeURIComponent(search)}`);
        console.log(res);
        if (res.data) {
          this.links = res.data;
        }
      } catch (e) {
        console.error(e)
      }

      this.renderGraph();
    },
    handleSearch() {
      this.fetchGraphData();
    },
    handleRelationClick(relationValue) {
      if (relationValue === 'show_all') {
        this.toggleAll();
      } else {
        this.toggleRelationship(relationValue);
      }
    },
    // AI转换的函数我不会别找我
    renderGraph() {
      // 清空原有svg
      if (this.svg) {
        this.svg.remove();
      }
      this.nodes = {};
      this.links.forEach(link => {
        link.source = this.nodes[link.source] || (this.nodes[link.source] = { name: link.source });
        link.target = this.nodes[link.target] || (this.nodes[link.target] = { name: link.target });
      });
      const width = 3000, height = 1800;
      // 绿色简约配色
      const colorList = ["#40c057", "#2da143", "#b9e7c3", "#d4f0d9", "#ebfbee", "#8b4513", "#a3e635", "#bef264", "#bbf7d0", "#22c55e"];
      const color = i => colorList[i % colorList.length];
      const nodesArr = Object.values(this.nodes);
      const linksArr = this.links.map(l => ({...l, source: l.source, target: l.target}));
      // d3-force模拟，减小排斥力，节点分布更轻松
      const simulation = d3.forceSimulation(nodesArr)
        .force("link", d3.forceLink(linksArr).distance(220).id(d => d.name))
        .force("charge", d3.forceManyBody().strength(-350))
        .force("center", d3.forceCenter(width / 2, height / 2));
      // 支持缩放和平移
      this.svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .call(d3.zoom()
          .scaleExtent([0.2, 2])
          .on("zoom", function (event) {
            g.attr("transform", event.transform);
          })
        );
      // 主g容器
      const g = this.svg.append("g");
      // 边
      const edges_line = g.append('g')
        .attr('class', 'edges')
        .selectAll(".edgepath")
        .data(linksArr)
        .enter()
        .append("line")
        .attr("stroke", "#40c057")
        .attr("stroke-width", 2);
      // 边文本
      const edges_text = g.append("g")
        .attr('class', 'edge-text')
        .selectAll(".edgelabel")
        .data(linksArr)
        .enter()
        .append("text")
        .attr("font-size", 18)
        .attr("fill", "#22c55e")
        .text(d => this.relationshipMap[d.rela] || '');
      // 节点
      const circle = g.append("g").selectAll("circle")
        .data(nodesArr)
        .enter().append("circle")
        .attr("r", 28)
        .attr("fill", (d, i) => color(i))
        .attr("stroke", "#fff")
        .attr("stroke-width", 3)
        .style("cursor", "pointer")
        .on("dblclick", node => this.navigateToNode(node.name))
        .on("mouseover", function () { d3.select(this).attr("r", 34); })
        .on("mouseout", function () { d3.select(this).attr("r", 28); })
        .call(d3.drag()
          .on("start", function(event, d) {
            if (!event.active) simulation.alphaTarget(0.2).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", function(event, d) {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", function(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
        );
      // 节点文本
      const text = g.append("g").selectAll("text.node-label")
        .data(nodesArr)
        .enter()
        .append("text")
        .attr("class", "node-label")
        .attr("font-size", 18)
        .attr("fill", "#1e293b")
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")
        .text(d => d.name);
      // tick函数
      simulation.on("tick", () => {
        circle.attr("cx", d => d.x = Math.max(40, Math.min(width - 40, d.x)))
              .attr("cy", d => d.y = Math.max(40, Math.min(height - 40, d.y)));
        text.attr("x", d => d.x)
            .attr("y", d => d.y + 6);
        edges_line.attr("x1", d => d.source.x)
                  .attr("y1", d => d.source.y)
                  .attr("x2", d => d.target.x)
                  .attr("y2", d => d.target.y);
        edges_text.attr("x", d => (d.source.x + d.target.x) / 2)
                  .attr("y", d => (d.source.y + d.target.y) / 2 - 10);
        this.updateCounts();
      });
      // 保存d3元素引用
      this.d3Elements = { circle, text, edges_line, edges_text };
      this.updateCounts();
    },
    // AI转换的函数我不会别找我
    navigateToNode(nodeName) {
      window.open("https://baike.baidu.com/item/" + nodeName, "_blank");
    },
    // AI转换的函数我不会别找我
    toggleRelationship(relationship) {
      const { edges_line, edges_text, circle, text } = this.d3Elements;
      // 找到相关边
      const relatedEdges = edges_line.filter(d => d.rela === relationship);
      // 相关节点
      const relatedNodes = new Set();
      relatedEdges.each(edge => {
        relatedNodes.add(edge.source.name);
        relatedNodes.add(edge.target.name);
      });
      // 隐藏所有
      edges_line.style("display", "none");
      edges_text.style("display", "none");
      circle.style("display", "none");
      text.style("display", "none");
      // 显示相关边
      relatedEdges.style("display", "inline");
      // 显示相关边的文本
      edges_text.filter(function(d) {
        return relatedEdges.filter(function(edge) {
          return edge.source === d.source && edge.target === d.target;
        }).size() > 0;
      }).style("display", "inline");
      // 显示相关节点
      circle.filter(d => relatedNodes.has(d.name)).style("display", "inline");
      text.filter(d => relatedNodes.has(d.name)).style("display", "inline");
      this.updateCounts();
    },
    // AI转换的函数我不会别找我
    toggleAll() {
      const { edges_line, edges_text, circle, text } = this.d3Elements;
      const isHidden = edges_line.style("display") === "none";
      const newDisplayState = isHidden ? "inline" : "none";
      edges_line.style("display", newDisplayState);
      edges_text.style("display", newDisplayState);
      circle.style("display", newDisplayState);
      text.style("display", newDisplayState);
      this.updateCounts();
    },
    updateCounts() {
      const { circle, edges_line } = this.d3Elements;
      this.nodeCount = circle ? circle.filter(function() { return d3.select(this).style("display") !== "none"; }).size() : 0;
      this.edgeCount = edges_line ? edges_line.filter(function() { return d3.select(this).style("display") !== "none"; }).size() : 0;
    }
  }
};
</script>

<style scoped lang="css">
.page-container {
  background-color: #ecf9ee;
}

* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: "微软雅黑", sans-serif;
}

*:focus {
  outline: none;
  box-shadow: 0 0 0 0.8rem rgba(34, 230, 93, 0.5);
}

/* 搜索区样式 */
.shift-mode {
  position: absolute;
  left: 50%;
  bottom: 20px;
  transform: translateX(-50%);
  padding: 12px 24px;
  background-color: #40c057;
  color: #fff;
  border-radius: 24px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-label {
  font-weight: 700;
  font-size: 1rem;
}

.search-input {
  padding: 10px 16px;
  border-radius: 12px;
  border: none;
  font-size: 0.95rem;
  width: 220px;
}

.search-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  background-color: #fff;
  color: #40c057;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background-color 0.2s;
}

.search-btn:hover {
  background-color: #f0fdf2;
}

/* 核心容器样式 */
.map-container {
  width: 100%;
  height: 100vh;
  display: grid;
  grid-template-columns: 2fr 8fr;
  background-color: #ecf9ee;
  /* 统一背景色，消除边边感 */
}

/* 左侧关系列表样式 */
.sidebar {
  background-color: #ecf9ee;
  overflow-y: auto;
  padding: 2rem 1rem;
}

.relation-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.relation-item {
  padding: 1.2rem 1.5rem;
  background-color: #ebfbee;
  border: 2px solid #40c057;
  border-radius: 18px;
  color: #1e293b;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  text-align: le;
}

.relation-item:hover {
  background-color: #d4f0d9;
  border-color: #2da143;
}

.relation-item:active {
  background-color: #b9e7c3;
}

/* 右侧图谱容器样式 */
.graph-container {
  background-color: #ecf9ee;
  /* 保持与整体一致 */
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.graph-content {
  background: rgb(236, 249, 238);
  width: 100%;
  height: 100%;
}

/* 滚动条样式 */
.sidebar::-webkit-scrollbar {
  width: 0.8rem;
}

.sidebar::-webkit-scrollbar-track {
  background-color: #ecf9ee;
  border-radius: 0.4rem;
}

.sidebar::-webkit-scrollbar-thumb {
  background-color: #c6eccd;
  border-radius: 0.4rem;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background-color: #b3e6bc;
}

.info {
  
  position: fixed;
  top: 10px;
  right: 300px;
  background: #a2d6ab;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  z-index: 1;
  font-size: 14px;
}

.edges line {
  stroke: #40c057;
  stroke-width: 2;
}

.node-label {
  font-size: 20px;
  fill: #1e293b;
  font-weight: bold;
  text-anchor: middle;
}

/* 节点绿色简约风格 */
svg circle {
  transition: r 0.2s;
  box-shadow: 0 2px 8px rgba(34, 230, 93, 0.15);
}
</style>