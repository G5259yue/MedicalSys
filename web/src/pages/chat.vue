<!-- 全AI生成的页面除了nvabar -->

<template>
  <div class="chat-page">
    <Nvabar />
    <div class="chat-container">
      <div v-if="messages.length" class="chat-history">
        <div v-for="(msg, idx) in messages" :key="idx" :class="msg.role === 'user' ? 'bubble user' : 'bubble ai'">
          <!-- <span v-if="msg.role === 'user'" class="bubble-label">我：</span> -->
          <span v-if="msg.role === 'ai'" class="bubble-label">医疗助手：</span>
          <span v-html="msg.text"></span>
        </div>
      </div>
      <div class="chat-input-bar">
        <input v-model="input" type="text" placeholder="请输入你的问题..." @keyup.enter="handleSend" class="chat-input" />
        <button class="send-btn" @click="handleSend">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Nvabar from './nvabar.vue';

export default {
  name: 'chat',
  components: { Nvabar },
  data() {
    return {
      input: '',
      messages: []
    };
  },
  mounted() {
    // 拦截 vue-link-btn 的点击，改为 router 跳转
    this.$nextTick(() => {
      this.addLinkInterception();
    });
  },
  updated() {
    // 每次渲染后都重新绑定
    this.addLinkInterception();
  },
  methods: {
    addLinkInterception() {
      // 只拦截 .vue-link-btn 链接
      const container = this.$el.querySelector('.chat-history');
      if (!container) return;
      const links = container.querySelectorAll('.vue-link-btn');
      links.forEach(link => {
        link.onclick = (e) => {
          e.preventDefault();
          const href = link.getAttribute('href');
          if (href) {
            this.$router.push(href);
          }
        };
      });
    },
    async handleSend() {
      const text = this.input.trim();
      if (!text) return;
      this.messages.push({ role: 'user', text });
      this.input = '';
      try {
        const res = await axios.post('/api/ask', null, {
          params: { msg: text }
        });
        this.messages.push({ role: 'ai', text: res.data.res });
        this.$nextTick(() => {
          const history = this.$el.querySelector('.chat-history');
          if (history) history.scrollTop = history.scrollHeight;
        });
      } catch (e) {
        this.messages.push({ role: 'ai', text: '网络错误，请稍后重试。' });
      }
    }
  }
};
</script>

<style scoped>
.chat-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #ecf9ee 0%, #d4f0d9 100%);
  display: flex;
  flex-direction: column;
}
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding-top: 80px;
  padding-bottom: 0;
}
.chat-history {
  width: 100%;
  max-width: 700px;
  flex: 1;
  overflow-y: auto;
  padding: 32px 0 120px 0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.bubble {
  max-width: 80%;
  padding: 18px 24px;
  border-radius: 18px;
  font-size: 18px;
  line-height: 1.6;
  word-break: break-word;
  box-shadow: 0 2px 8px rgba(34, 230, 93, 0.08);
  position: relative;
  margin-left: 16px;
  margin-right: 16px;
}
.bubble.user {
  background: #40c057;
  color: #fff;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}
.bubble.ai {
  background: #fff;
  color: #1e293b;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  border: 1.5px solid #40c057;
}
.bubble-label {
  font-size: 14px;
  font-weight: 700;
  margin-right: 8px;
  color: #22c55e;
}
.chat-input-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: #ecf9ee;
  box-shadow: 0 -2px 8px rgba(34, 230, 93, 0.08);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 18px 0;
  z-index: 100;
}
.chat-input {
  width: 480px;
  padding: 14px 18px;
  border-radius: 12px;
  border: 2px solid #40c057;
  font-size: 18px;
  margin-right: 16px;
  background: #fff;
  color: #1e293b;
  outline: none;
  transition: border 0.2s;
}
.chat-input:focus {
  border: 2px solid #22c55e;
}
.send-btn {
  padding: 14px 32px;
  border: none;
  border-radius: 12px;
  background-color: #40c057;
  color: #fff;
  font-weight: 700;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
}
.send-btn:hover {
  background-color: #22c55e;
}

.vue-link-btn {
  display: inline-block;
  background: #40c057;
  color: #fff !important;
  border-radius: 8px;
  padding: 6px 18px;
  margin: 0 4px;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.2s;
  border: none;
  cursor: pointer;
}
.vue-link-btn:hover {
  background: #22c55e;
  color: #fff !important;
}
</style>