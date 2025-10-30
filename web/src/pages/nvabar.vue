<template>
  <header class="navbar">
    <div class="navbar-left">
      <span class="navbar-title">医疗助手</span>
    </div>
    <nav class="navbar-right">
      <ul class="navbar-list">
        <li><router-link to="/" class="navbar-link">主页</router-link></li>
        <li><router-link to="/introduce" class="navbar-link">介绍</router-link></li>
        <li><a href="http://localhost:7474" class="navbar-link">数据库</a></li>
        <li>
          <a href="https://github.com/BaxterL/MedicalSys" class="navbar-link github-link" target="_blank" title="GitHub">
            <i class="fa fa-github"></i>
          </a>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
.navbar {
  width: 100%;
  height: 64px;
  /* background: linear-gradient(90deg, #5fe477 0%, #ecf9ee 100%); */
  background-color: #ecf9ee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.08);
  padding: 0 40px;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}
.navbar-left {
  display: flex;
  align-items: center;
}
.navbar-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  letter-spacing: 2px;
  text-shadow: 0 2px 8px rgba(34, 230, 93, 0.15);
}
.navbar-right {
  display: flex;
  align-items: center;
}
.navbar-list {
  display: flex;
  list-style: none;
  gap: 32px;
  align-items: center;
  margin: 0;
  padding: 0;
}
.navbar-link {
  text-decoration: none;
  color: #333;
  font-size: 18px;
  font-weight: 500;
  padding: 6px 16px;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
  background: rgba(255,255,255,0.0);
}
.navbar-link:hover {
  background: #d4f0d9;
  color: #40c057;
}
.github-link {
  padding: 6px 10px;
}
.fa-github {
  font-size: 22px;
  color: #333;
  transition: color 0.2s;
}
.github-link:hover .fa-github {
  color: #40c057;
}
</style>