<script setup>
import { onMounted, ref } from 'vue';
import { fetchAuditLogs } from '@/api/platform';
import { formatDateTime } from '@/shared/utils/formatters';

const loading = ref(false);
const errorMessage = ref('');
const logs = ref([]);

const columns = [
  { colKey: 'created_at_text', title: '时间' },
  { colKey: 'action', title: '动作' },
  { colKey: 'actor_name', title: '操作者' },
  { colKey: 'actor_role', title: '角色' },
  { colKey: 'target_type', title: '目标类型' },
  { colKey: 'target_id', title: '目标ID' },
  { colKey: 'detail_json', title: '详情' },
];

async function loadAuditLogs() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const data = await fetchAuditLogs();
    logs.value = data.map((item) => ({
      ...item,
      created_at_text: formatDateTime(item.created_at),
      detail_json: item.detail_json || '-',
      actor_name: item.actor_name || '-',
      actor_role: item.actor_role || '-',
      target_type: item.target_type || '-',
      target_id: item.target_id ?? '-',
    }));
  } catch (error) {
    errorMessage.value = error.message || '读取审计日志失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadAuditLogs);
</script>

<template>
  <div class="page-view audit-page">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-card class="page-card audit-hero" :bordered="false">
      <div class="hero-row">
        <div>
          <h3>审计日志中心</h3>
          <p>记录登录、模型调用、客户端结果回传和系统初始化等关键事件，方便答辩演示与问题排查。</p>
        </div>
        <t-button theme="primary" :loading="loading" @click="loadAuditLogs">刷新日志</t-button>
      </div>
    </t-card>
    <t-card class="page-card translucent-card" title="最近 100 条审计日志">
      <t-table row-key="id" :data="logs" :columns="columns" :hover="true" :loading="loading" />
    </t-card>
  </div>
</template>

<style scoped lang="scss">
.audit-page {
  gap: 18px;
}

.audit-hero {
  padding: 20px;
  background:
    radial-gradient(circle at 90% 10%, rgba(168, 85, 247, 0.14), transparent 28%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(250, 245, 255, 0.92));
}

.hero-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}

.hero-row h3 {
  margin: 0 0 6px;
  font-size: 22px;
}

.hero-row p {
  margin: 0;
  color: var(--app-text-sub);
}

.translucent-card {
  background: rgba(255, 255, 255, 0.84);
}
</style>
