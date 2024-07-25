import { createRouter, createWebHistory } from 'vue-router';
import OneView from './components/OneView';
import TwoView from './components/TwoView';
import TestView from './components/TestView.vue';
import HomeView from './components/HomeView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'One',
      path: '/one',
      component: OneView
    },
    {
      name: 'Two',
      path: '/two',
      component: TwoView
    },
    {
      name: 'Test',
      path: '/test',
      component: TestView
    },
    {
      name: 'Home',
      path: '/',
      component: HomeView
    },
  ],
});

export default router;