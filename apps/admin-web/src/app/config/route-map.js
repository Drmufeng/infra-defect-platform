// 路由配置集中管理：
// 1. 页面组件统一使用动态导入，保证按需懒加载
// 2. 菜单分组、标题与组件路径在同一处维护，减少重复配置
export const adminRouteGroups = [
  {
    section: {
      value: 'overview',
      title: '总览区',
      icon: 'app',
    },
    routes: [
      {
        path: '/dashboard',
        name: 'dashboard',
        title: '工作台',
        icon: 'dashboard',
        component: () => import('@/pages/dashboard/index.vue'),
      },
      {
        path: '/models',
        name: 'models',
        title: '模型管理',
        icon: 'root-list',
        component: () => import('@/pages/models/index.vue'),
      },
      {
        path: '/settings',
        name: 'settings',
        title: '系统设置',
        icon: 'setting',
        component: () => import('@/pages/settings/index.vue'),
      },
    ],
  },
  {
    section: {
      value: 'dataset-center',
      title: '数据与训练',
      icon: 'database',
    },
    routes: [
      {
        path: '/datasets',
        name: 'datasets',
        title: '数据集管理',
        icon: 'server',
        component: () => import('@/pages/datasets/index.vue'),
      },
      {
        path: '/training',
        name: 'training',
        title: '模型训练',
        icon: 'chart',
        component: () => import('@/pages/training/index.vue'),
      },
    ],
  },
  {
    section: {
      value: 'client-collaboration',
      title: '客户端协同',
      icon: 'secured',
    },
    routes: [
      {
        path: '/client-access',
        name: 'client-access',
        title: '客户端接入管理',
        icon: 'secured',
        component: () => import('@/pages/client-access/index.vue'),
      },
    ],
  },
  {
    section: {
      value: 'ops-center',
      title: '资产与审计',
      icon: 'folder-open',
    },
    routes: [
      {
        path: '/artifacts',
        name: 'artifacts',
        title: '文件资产',
        icon: 'file-copy',
        component: () => import('@/pages/artifacts/index.vue'),
      },
      {
        path: '/audit-logs',
        name: 'audit-logs',
        title: '审计日志',
        icon: 'time-history',
        component: () => import('@/pages/audit-logs/index.vue'),
      },
    ],
  },
  {
    section: {
      value: 'inference-center',
      title: '测试与验证',
      icon: 'precise-monitor',
    },
    routes: [
      {
        path: '/testing',
        name: 'testing',
        title: '推理测试',
        icon: 'play-circle',
        component: () => import('@/pages/testing/index.vue'),
      },
    ],
  },
];


export const flatAdminRoutes = adminRouteGroups.flatMap((group) => group.routes);
