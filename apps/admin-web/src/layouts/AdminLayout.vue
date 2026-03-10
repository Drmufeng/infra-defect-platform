<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchCurrentUser } from '@/api/platform';
import { adminMenuSections, getDefaultExpanded } from '@/app/config/navigation';
import { clearAuthSession, getStoredUser } from '@/shared/utils/auth';

const route = useRoute();
const router = useRouter();

// 折叠状态只控制侧边栏宽度与菜单展示，不影响路由和数据逻辑。
const collapsed = ref(false);

// 展开的分组单独维护，便于后续根据用户习惯或权限动态调整。
const expanded = ref(getDefaultExpanded());

const activePath = computed(() => route.path);
const currentUser = ref(getStoredUser());

// 切换菜单项时统一使用路由跳转，避免页面自己处理导航逻辑。
const handleMenuChange = (value) => {
  if (typeof value === 'string' && value.startsWith('/')) {
    router.push(value);
  }
};

const toggleCollapsed = () => {
  collapsed.value = !collapsed.value;
};

const handleLogout = () => {
  clearAuthSession();
  router.replace('/login');
};

async function syncCurrentUser() {
  try {
    currentUser.value = await fetchCurrentUser();
  } catch {
    clearAuthSession();
    router.replace('/login');
  }
}

// 当路由变化时，自动确保对应分组已展开，减少用户找页面的成本。
watch(
  () => route.path,
  (path) => {
    const matchedSection = adminMenuSections.find((section) => section.children.some((item) => item.value === path));
    if (matchedSection && !expanded.value.includes(matchedSection.value)) {
      expanded.value = [...expanded.value, matchedSection.value];
    }
  },
  { immediate: true },
);

onMounted(syncCurrentUser);
</script>

<template>
  <t-layout class="admin-shell">
    <t-aside :width="collapsed ? '92px' : '272px'" class="admin-aside">
      <div class="brand-block">
        <div class="brand-logo">RD</div>
        <div v-if="!collapsed" class="brand-text">
          <strong>病害检测后台</strong>
          <span>Road Damage Admin</span>
        </div>
      </div>

      <t-menu
        v-model:expanded="expanded"
        theme="light"
        :value="activePath"
        expand-mutex
        :collapsed="collapsed"
        class="admin-menu"
        @change="handleMenuChange"
      >
        <t-submenu v-for="section in adminMenuSections" :key="section.value" :value="section.value">
          <template #icon>
            <t-icon :name="section.icon" />
          </template>
          <template #title>
            <span>{{ section.title }}</span>
          </template>

          <t-menu-item v-for="item in section.children" :key="item.value" :value="item.value">
            <template #icon>
              <t-icon :name="item.icon" />
            </template>
            {{ item.label }}
          </t-menu-item>
        </t-submenu>

        <template #operations>
          <t-button variant="text" shape="square" class="menu-collapse-btn" @click="toggleCollapsed">
            <template #icon>
              <t-icon name="view-list" />
            </template>
          </t-button>
        </template>
      </t-menu>
    </t-aside>

    <t-layout>
      <t-header class="admin-header">
        <div class="header-left">
          <div>
            <h2>{{ route.meta.title || '后台管理' }}</h2>
            <p>基于 Vue3 + TDesign 的基础设施病害智能检测管理端</p>
          </div>
        </div>

        <div class="header-right">
          <t-tag theme="success" variant="light">模型已可用</t-tag>
          <t-tag theme="primary" variant="light">{{ currentUser?.username || '未登录' }}</t-tag>
          <t-tag theme="warning" variant="light">{{ currentUser?.role || '-' }}</t-tag>
          <t-button variant="outline" size="small" @click="handleLogout">退出</t-button>
        </div>
      </t-header>

      <t-content class="admin-content">
        <router-view />
      </t-content>
    </t-layout>
  </t-layout>
</template>

<style scoped lang="scss">
.admin-shell {
  min-height: 100vh;
}

.admin-aside {
  display: flex;
  flex-direction: column;
  padding: 20px 14px 12px;
  background: rgba(255, 255, 255, 0.82);
  border-right: 1px solid var(--app-border);
  box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.3);
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 10px 22px;
}

.brand-logo {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  color: #fff;
  font-weight: 700;
  background: linear-gradient(135deg, #0052d9, #2f7cff);
  border-radius: 14px;
  box-shadow: 0 10px 22px rgba(0, 82, 217, 0.28);
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-text span {
  font-size: 12px;
  color: var(--app-text-sub);
}

.admin-menu {
  flex: 1;
  background: transparent;
}

.menu-collapse-btn {
  color: var(--app-brand);
}

.menu-collapse-btn:hover {
  background: rgba(0, 82, 217, 0.08);
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: auto;
  padding: 24px 28px 0;
  background: transparent;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
  font-size: 28px;
}

.header-left p {
  margin: 4px 0 0;
  color: var(--app-text-sub);
}

.admin-content {
  padding: 24px 28px 28px;
}

@media (max-width: 900px) {
  .admin-header {
    flex-direction: column;
    align-items: stretch;
    padding: 20px 16px 0;
  }

  .admin-content {
    padding: 16px;
  }

  .header-left,
  .header-right {
    flex-wrap: wrap;
  }
}
</style>
