<template>
  <div class="homepage">
    <!-- 导航栏 -->
    <!-- <header class="header">
      <router-link :to="{ path: '/' }">
        <img class="logo" src="/static/img/Graph_Vocab.png" alt="Logo" />
      </router-link>
      
      <nav class="main-nav">
        <ul class="main-nav-list">
          <li class="search-box">
            <input 
              class="search-txt" 
              type="text" 
              placeholder="搜索单词..." 
              v-model="searchText"
              @keyup.enter="handleSearch"
            />
            <button class="search-btn" @click="handleSearch">
              <i class="icon-search"></i>
            </button>
          </li>
          <li><router-link to="/main" class="main-nav-link">开始学习</router-link></li>
          <li><a href="https://github.com/Nozom1466" class="main-nav-link">GitHub</a></li>
          <li><router-link to="/login" class="main-nav-link nav-cta">登录</router-link></li>
        </ul>
      </nav>
    </header> -->
    <Nvabar></Nvabar>
    <!-- 主内容区 -->
    <main class="main-content">
      <section class="hero-section">
        <div class="hero-container">
          <div class="hero-image-box grid--5-cols grid--5-rows">
            <!-- 第一张图片 -->
            <div class="hero-img hero-img-1">
              <img src="/static/img/hero1.png" alt="词汇学习插图1" class="hero-img" />
            </div>

            <!-- 星期显示 -->
            <p class="week">{{ weekday }}</p>

            <!-- 日期显示 -->
            <p class="weekanddata" v-html="dateStr"></p>

            <!-- 第二张图片 -->
            <div class="hero-img hero-img-2">
              <img src="/static/img/hero2.png" alt="词汇学习插图2" class="hero-img" />
            </div>
          </div>

          <div class="hero-text-box">
            <h1 class="main-title">
              在<span class="highlight">图谱</span>中探索，
              为你量身定制的医疗助手
            </h1>
            <p class="description">
              基于知识图谱的医疗可视化及问答系统
            </p>
            <div class="action-buttons">
              <router-link to="/chat" class="btn primary-btn">开始使用</router-link>
              <router-link to="/main" class="btn outline-btn">数据可视化</router-link>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <!-- <footer class="footer">
      <div class="footer-content">
        <p>2025 CQCFE</p>
      </div>
    </footer> -->
  </div>
</template>

<script>
import Nvabar from './nvabar.vue';

export default {
  name: 'HomePage',
  data() {
    return {
      searchText: '',
      weekday: '',
      dateStr: '' // 最终格式为 "月份<br>日期+后缀"
    }
  },
  mounted() {
    this.setDateInfo();
  },
  components: {
    Nvabar
  },
  methods: {
    setDateInfo() {
      const today = new Date();
      const weekdays = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
      const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

      // 处理星期（如 "WED."）
      this.weekday = weekdays[today.getDay()] + '.';

      // 处理日期和月份：用<br>实现换行
      const date = today.getDate();
      const month = months[today.getMonth()]; // 如 "OCT"
      // 日期后缀逻辑不变
      const suffix = date % 10 === 1 ? 'st' :
        date % 10 === 2 ? 'nd' :
          date % 10 === 3 ? 'rd' : 'th';

      // 拼接为 "月份<br>日期+后缀" 格式（如 "OCT<br>29st"）
      this.dateStr = `${month}<br>${date}${suffix}`;
    },
    handleSearch() {
      if (this.searchText.trim()) {
        this.$router.push({
          path: '/search',
          query: { word: this.searchText }
        });
      }
    }
  }
}
</script>

<style scoped>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: sans-serif;
  line-height: 1.6;
}

/* 导航栏
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 48px;
  height: 96px;
  background-color: #ecf9ee;
}

.logo {
  height: 100px;
}

.main-nav-list {
  display: flex;
  list-style: none;
  gap: 32px;
  align-items: center;
}

.main-nav-link {
  text-decoration: none;
  color: #333;
  font-size: 16px;
  font-weight: 500;
  transition: color 0.3s;
}

.main-nav-link:hover {
  color: #40c057;
}

.nav-cta {
  padding: 10px 20px;
  background-color: #40c057;
  color: white;
  border-radius: 6px;
}

.nav-cta:hover {
  background-color: #339a46;
  color: white;
} */

/* 搜索框 */
/* .search-box {
  display: flex;
  align-items: center;
  background-color: #40c057;
  border-radius: 40px;
  padding: 6px;
}

.search-txt {
  border: none;
  background: transparent;
  outline: none;
  color: white;
  width: 0;
  transition: width 0.4s;
  font-size: 14px;
}

.search-box:hover .search-txt {
  width: 200px;
  padding: 0 12px;
}

.search-btn {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: background-color 0.4s, color 0.4s;
}

.search-box:hover .search-btn {
  background-color: white;
  color: #40c057;
} */

/* 主内容区 */
.main-content {
  background-color: #ebfbee;
  padding: 80px 0;
}

.hero-section {
  background-color: #ebfbee;
  padding: 48px 0 96px 0;
  height: 85vh;
}

.hero-container {
  width: 100%;
  margin: 0 auto;
  padding: 0 80px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: center;
  min-height: 100%;
}


/* 左侧图片区 */

/* 这啥 */

.img {
    overflow-clip-margin: content-box;
    overflow: clip;
}

.grid--5-rows {
  grid-template-rows: repeat(2, 1fr);
}

.grid--5-cols {
  grid-template-columns: 2fr repeat(3, 1fr) 2fr;
}

.hero-image-box {
  display: grid;
  row-gap: 16px;
  z-index: 0;
}

.hero-img {
    width: 100%;
    border-radius: 9px;
}
.image-wrapper {
  
  width: 100%;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
}

/* .image-wrapper:first-child {
  grid-column: 1 / 3;
  grid-row: 1 / 2;
}

.image-wrapper:last-child {
  grid-column: 2 / 4;
  grid-row: 2 / 3;
} */

.hero-img-1 {
  grid-row: 1 / 2;
  grid-column: 1 / 4;
}

.hero-img-2 {
  grid-row: 2 / 3;
  grid-column: 3 / -1;
}

.date-display {
  grid-column: 3 / 4;
  grid-row: 1 / 2;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.week {
  font-size: 86px;
  font-weight: 600;
  color: #c6eccd;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  grid-row: 1 / 2;
  grid-column: 4 / -1;
}

.weekanddata {
  font-size: 86px;
  font-weight: 600;
  color: #c6eccd;
  margin-bottom: 0px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  align-self: end;
  padding-right: 5px;
  grid-row: 2 / 3;
  grid-column: 1 / 3;
}

/* 右侧文本区 */
.hero-text-box {
  text-align: center;
  padding: 20px;
}

.main-title {
  font-size: 74px;
  margin-bottom: 100px;
  line-height: 1.2;
}

.highlight {
  color: #339a46;
}

.description {
  font-size: 30px;
  margin-bottom: 32px;
  color: #666;
}

/* 按钮样式 */
.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  text-decoration: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s;
}

.primary-btn {
  background-color: #40c057;
  color: white;
}

.primary-btn:hover {
  background-color: #339a46;
}

.outline-btn {
  background-color: white;
  color: #555;
  border: 2px solid transparent;
}

.outline-btn:hover {
  background-color: #ecf9ee;
  box-shadow: inset 0 0 0 2px white;
}

/* 页脚 */
.footer {
  background-color: #ecf9ee;
  padding: 24px 0;
  text-align: center;
}

.footer-content {
  color: #666;
  font-size: 14px;
}
</style>