<template>
    <div class="bg">
        <Nvabar />
        <div class="introduce-container">
            <MarkdownRender :content="content" />
        </div>
    </div>
</template>

<script>
import Nvabar from './nvabar.vue';
import MarkdownRender from 'vue-renderer-markdown'

export default {
    name: 'introduce',
    components: {
        Nvabar,
        MarkdownRender
    },
    data() {
        return {
            content: ''
        }
    },
    mounted() {
        fetch('/static/md/info.md')
            .then(res => res.text())
            .then(md => {
                this.content = md;
            });
    }
}
</script>

<style scoped>
@import './render.css';
.bg {
    min-height: 100vh;
    background-color: #ebfbee;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.introduce-container {
    margin-top: 80px;
    padding: 48px;
    max-width: 800px;
    width: 100%;
    font-size: 18px;
    line-height: 1.6;
    color: #222;
    background: #fff;
    border-radius: 20px;
    box-shadow: 0 2px 12px rgba(34, 34, 34, 0.194);
}
</style>