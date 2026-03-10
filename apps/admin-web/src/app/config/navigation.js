import { adminRouteGroups } from '@/app/config/route-map';

// 菜单结构直接从路由配置派生，避免导航和路由各维护一份造成不一致。
export const adminMenuSections = adminRouteGroups.map((group) => ({
  value: group.section.value,
  title: group.section.title,
  icon: group.section.icon,
  children: group.routes.map((route) => ({
    value: route.path,
    label: route.title,
    icon: route.icon,
  })),
}));

export const getDefaultExpanded = () => adminMenuSections.map((item) => item.value);
