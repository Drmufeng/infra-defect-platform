import { createRouter, createWebHashHistory } from 'vue-router';
import AdminLayout from '@/layouts/AdminLayout.vue';
import { flatAdminRoutes } from '@/app/config/route-map';
import { isLoggedIn } from '@/shared/utils/auth';

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/login/index.vue'),
    meta: { title: '登录' },
  },
  {
    path: '/',
    component: AdminLayout,
    redirect: '/dashboard',
    children: flatAdminRoutes.map((route) => ({
      path: route.path.replace(/^\//, ''),
      name: route.name,
      component: route.component,
      meta: { title: route.title },
    })),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});

router.beforeEach((to) => {
  const loggedIn = isLoggedIn();
  if (to.path !== '/login' && !loggedIn) {
    return '/login';
  }
  if (to.path === '/login' && loggedIn) {
    return '/dashboard';
  }
  return true;
});

export default router;
