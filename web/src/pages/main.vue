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
        <div id="graphArea" class="graph-content"></div>
          <div class="tool" style="position: absolute; top: -0.0001762px; left: 411.273px; border-radius: 10px; padding: 10px 20px; width: 360px;"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MedicalNeo4jGraph",
  data() {
    return {
      diseaseKeyword: "",
      relationList: [
        { value: "acompany_with", label: "伴随" ,desc:"会伴随节点的疾病"},
        { value: "belongs_to", label: "属于" ,desc:"test"},
        { value: "common_drug", label: "常用药物" ,desc:"test"},
        { value: "do_eat", label: "宜食" ,desc:"test"},
        { value: "drugs_of", label: "药物" ,desc:"test"},
        { value: "has_symptom", label: "有症状" ,desc:"test"},
        { value: "need_check", label: "需要检查" ,desc:"test"},
        { value: "no_eat", label: "忌食" ,desc:"test"},
        { value: "recommand_drug", label: "推荐药物" ,desc:"test"},
        { value: "recommand_eat", label: "推荐饮食" ,desc:"test"},
        { value: "show_all", label: "显示全部" ,desc:"test"}
      ]
    };
  },
  methods: {
    handleSearch() {
      const keyword = this.diseaseKeyword.trim();
      if (!keyword) return;
      console.log("搜索疾病：", keyword);
    },
    handleRelationClick(relationValue) {
      console.log("触发关系：", relationValue);
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
</style>