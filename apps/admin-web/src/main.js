import { createApp } from 'vue';
import TDesign from 'tdesign-vue-next';
import App from './App.vue';
import router from './app/router';
import 'tdesign-vue-next/es/style/index.css';
import './assets/styles/global.scss';

// 通过全局注册 TDesign 组件，避免在当前阶段引入额外的自动导入配置，
// 这样能减少依赖解析问题，也更方便后续逐步接入真实业务代码。
createApp(App).use(router).use(TDesign).mount('#app');
