<template>
  <div class="page-container">
    <!-- 顶部导航栏 -->
    <header class="header">
      <img 
        class="logo" 
        src="static/img/logo.png" 
        alt="Medical KG System"
      />
      <nav class="main-nav">
        <ul class="main-nav-list">
          <li class="search-box">
            <input
              class="search-txt"
              type="text"
              placeholder="输入查询内容..."
              v-model="queryText"
              @keyup.enter="searchKG"
            />
            <button class="search-btn" @click="searchKG">
              <i class="icon iconfont icon-search"></i>
            </button>
          </li>
          <li>
            <a class="main-nav-link" href="#" @click.prevent="resetGraph">重置图谱</a>
          </li>
          <li>
            <a class="main-nav-link" href="#" @click.prevent="showHelp">使用帮助</a>
          </li>
        </ul>
      </nav>
    </header>

    <!-- 主要内容区 -->
    <main class="main-content">
      <!-- 左侧边栏 -->
      <div class="sidebar">
        <div class="sidebar-header">
          <h2>查询结果</h2>
          <div class="result-count">找到 {{ resultCount }} 个相关实体</div>
        </div>
        
        <ul class="entity-list">
          <li 
            v-for="(entity, index) in entities" 
            :key="index"
            class="entity-item"
            @click="focusEntity(entity)"
          >
            <div class="entity-name">{{ entity.name }}</div>
            <div class="entity-type">{{ entity.type }}</div>
          </li>
        </ul>
      </div>

      <!-- 中间图谱区域 -->
      <div class="graph-container">
        <div id="graphArea"></div>
      </div>

      <!-- 右侧信息面板 -->
      <div class="info-panel">
        <div v-if="selectedEntity" class="entity-detail">
          <h3 class="detail-title">{{ selectedEntity.name }}</h3>
          <div class="detail-type">{{ selectedEntity.type }}</div>
          
          <div class="detail-section">
            <h4>属性信息</h4>
            <ul class="property-list">
              <li v-for="(value, key) in selectedEntity.properties" :key="key">
                <span class="property-key">{{ key }}:</span>
                <span class="property-value">{{ value }}</span>
              </li>
            </ul>
          </div>
          
          <div class="detail-section">
            <h4>关系信息</h4>
            <ul class="relation-list">
              <li v-for="(relation, idx) in selectedEntity.relations" :key="idx">
                <span class="relation-name">{{ relation.name }}</span>
                <span class="relation-target" @click="focusEntity(relation.target)">{{ relation.target.name }}</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <p>请点击图谱中的实体查看详情</p>
        </div>
      </div>
    </main>

    <!-- 底部控制栏 -->
    <div class="control-bar">
      <div class="control-group">
        <button class="control-btn" @click="zoomIn">
          <i class="icon iconfont icon-zoom-in"></i> 放大
        </button>
        <button class="control-btn" @click="zoomOut">
          <i class="icon iconfont icon-zoom-out"></i> 缩小
        </button>
        <button class="control-btn" @click="fitView">
          <i class="icon iconfont icon-reset"></i> 适应视图
        </button>
      </div>
      
      <div class="layout-controls">
        <label class="layout-label">布局方式:</label>
        <select class="layout-select" v-model="layoutType" @change="changeLayout">
          <option value="force">力导向布局</option>
          <option value="circular">环形布局</option>
          <option value="hierarchical">层次布局</option>
        </select>
      </div>
    </div>

    <!-- 帮助弹窗 -->
    <div v-if="showHelpModal" class="modal-backdrop">
      <div class="modal">
        <div class="modal-header">
          <h3>使用帮助</h3>
          <button class="close-btn" @click="showHelpModal = false">×</button>
        </div>
        <div class="modal-content">
          <p>1. 在顶部搜索框输入医疗实体名称进行查询</p>
          <p>2. 点击左侧实体列表可定位到图谱中的实体</p>
          <p>3. 点击图谱中的实体可在右侧查看详细信息</p>
          <p>4. 可通过底部控制按钮调整图谱显示方式</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import '../assets/lib/jquery-3.2.1/jquery-3.2.1.min.js'
import '../assets/lib/interactive-graph-0.1.0/interactive-graph.min.js'

export default {
  name: 'MedicalKGView',
  data() {
    return {
      queryText: '',
      entities: [],
      resultCount: 0,
      selectedEntity: null,
      graphApp: null,
      layoutType: 'force',
      showHelpModal: false
    }
  },
  mounted() {
    this.initGraph()
  },
  methods: {
    // 初始化图谱
    initGraph() {
      igraph.i18n.setLanguage("chs");
      this.graphApp = new igraph.GraphNavigator(
        document.getElementById("graphArea"),
        {
          canvasBackground: "#ecf9ee",
          nodes: {
            color: "#40c057",
            size: 20,
            labelFontSize: 14
          },
          edges: {
            color: "#a5d8a7",
            width: 2,
            labelFontSize: 12
          },
          groups: {
            useSeqColors: false,
            custom: {
              疾病: { color: '#e53e3e' },
              症状: { color: '#ed8936' },
              药物: { color: '#3182ce' },
              检查: { color: '#805ad5' },
              治疗: { color: '#38a169' }
            }
          }
        }
      )

      // 绑定实体点击事件
      this.graphApp.on('nodeClick', (node) => {
        this.fetchEntityDetail(node.id)
      })

      this.hideUselessControls()
    },

    // 隐藏不需要的控件
    hideUselessControls() {
      const toolBar = document.querySelector('.toolbarPanel')
      const searchPanel = document.querySelector('.searchPanel')
      
      if (toolBar) toolBar.style.display = 'none'
      if (searchPanel) searchPanel.style.display = 'none'
    },

    // 搜索知识图谱
    searchKG() {
      if (!this.queryText.trim()) return

      // 实际项目中替换为真实接口
      fetch(`/api/kg/search?query=${this.queryText}`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            this.entities = data.entities
            this.resultCount = data.entities.length
            this.graphApp.loadGson(data.graphData)
          }
        })
        .catch(err => console.error('搜索失败:', err))
    },

    // 聚焦实体
    focusEntity(entity) {
      this.graphApp.pickup([{ id: entity.id }])
      this.fetchEntityDetail(entity.id)
    },

    // 获取实体详情
    fetchEntityDetail(entityId) {
      // 实际项目中替换为真实接口
      fetch(`/api/kg/entity/${entityId}`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            this.selectedEntity = data.entity
          }
        })
    },

    // 重置图谱
    resetGraph() {
      this.graphApp.clear()
      this.entities = []
      this.resultCount = 0
      this.selectedEntity = null
      this.queryText = ''
    },

    // 图谱控制方法
    zoomIn() {
      this.graphApp.zoomIn()
    },
    zoomOut() {
      this.graphApp.zoomOut()
    },
    fitView() {
      this.graphApp.fitView()
    },
    changeLayout() {
      this.graphApp.setLayout(this.layoutType)
    },

    // 显示帮助
    showHelp() {
      this.showHelpModal = true
    }
  }
}
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background-color: #f8f9fa;
}

/* 头部样式 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ecf9ee;
  height: 96px;
  padding: 0 48px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.logo {
  height: 80px;
}

.main-nav-list {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 24px;
}

.main-nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 16px;
  transition: all 0.3s;
  padding: 8px 12px;
  border-radius: 4px;
}

.main-nav-link:hover {
  color: #40c057;
  background-color: rgba(64, 192, 87, 0.1);
}

/* 搜索框样式 */
.search-box {
  padding: 6px;
  border-radius: 40px;
  background-color: #40c057;
  display: flex;
  align-items: center;
}

.search-txt {
  border: none;
  background: none;
  outline: none;
  font-size: 16px;
  color: #fff;
  line-height: 1;
  width: 0;
  transition: width 0.4s;
}

.search-box:hover .search-txt {
  width: 240px;
  padding: 0 12px;
}

.search-txt::placeholder {
  color: rgba(255, 255, 255, 0.8);
}

.search-btn {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.4s;
}

.search-box:hover .search-btn {
  background-color: white;
  color: #40c057;
}

/* 主内容区样式 */
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: 280px;
  background-color: #fff;
  border-right: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e9ecef;
}

.sidebar-header h2 {
  color: #333;
  font-size: 18px;
  margin-bottom: 8px;
}

.result-count {
  color: #666;
  font-size: 14px;
}

.entity-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.entity-item {
  padding: 12px;
  margin-bottom: 8px;
  background-color: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.entity-item:hover {
  background-color: #ecf9ee;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.entity-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.entity-type {
  font-size: 12px;
  color: #666;
  background-color: rgba(64, 192, 87, 0.1);
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
}

/* 图谱容器样式 */
.graph-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background-color: #ecf9ee;
}

#graphArea {
  width: 100%;
  height: 100%;
}

/* 信息面板样式 */
.info-panel {
  width: 320px;
  background-color: #fff;
  border-left: 1px solid #e9ecef;
  overflow-y: auto;
  padding: 16px;
}

.detail-title {
  color: #333;
  font-size: 20px;
  margin-bottom: 4px;
}

.detail-type {
  color: #40c057;
  font-size: 14px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e9ecef;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  color: #555;
  font-size: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.detail-section h4::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 16px;
  background-color: #40c057;
  margin-right: 8px;
  border-radius: 2px;
}

.property-list, .relation-list {
  list-style: none;
}

.property-list li {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #f1f1f1;
}

.property-key {
  display: inline-block;
  width: 80px;
  color: #666;
  font-weight: 500;
}

.property-value {
  color: #333;
}

.relation-list li {
  margin-bottom: 12px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.relation-name {
  color: #e53e3e;
  font-weight: 500;
  margin-right: 8px;
}

.relation-target {
  color: #3182ce;
  cursor: pointer;
}

.relation-target:hover {
  text-decoration: underline;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 16px;
}

/* 控制栏样式 */
.control-bar {
  height: 60px;
  background-color: #fff;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
}

.control-group {
  display: flex;
  gap: 12px;
}

.control-btn {
  background-color: #ecf9ee;
  color: #333;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.control-btn:hover {
  background-color: #40c057;
  color: #fff;
}

.layout-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.layout-label {
  color: #666;
  font-size: 14px;
}

.layout-select {
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background-color: #fff;
}

/* 帮助弹窗样式 */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  width: 500px;
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 16px 24px;
  background-color: #ecf9ee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #333;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
}

.modal-content {
  padding: 24px;
}

.modal-content p {
  margin-bottom: 12px;
  line-height: 1.6;
}
</style>