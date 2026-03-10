<script setup>
import { computed, onMounted, ref } from 'vue';
import { fetchArtifacts } from '@/api/platform';
import { formatDateTime } from '@/shared/utils/formatters';

const loading = ref(false);
const errorMessage = ref('');
const artifacts = ref([]);

const columns = [
  { colKey: 'file_name', title: '文件名' },
  { colKey: 'owner_type', title: '归属类型' },
  { colKey: 'file_type', title: '文件类型' },
  { colKey: 'file_size_text', title: '大小' },
  { colKey: 'created_by', title: '创建人' },
  { colKey: 'created_at_text', title: '创建时间' },
  { colKey: 'file_path', title: '路径' },
];

const assetStats = computed(() => ({
  total: artifacts.value.length,
  weightCount: artifacts.value.filter((item) => item.file_type === 'weight').length,
  reportCount: artifacts.value.filter((item) => item.file_type === 'report').length,
}));

function formatFileSize(value) {
  if (!value && value !== 0) {
    return '-';
  }
  if (value < 1024) {
    return `${value} B`;
  }
  if (value < 1024 * 1024) {
    return `${(value / 1024).toFixed(1)} KB`;
  }
  return `${(value / (1024 * 1024)).toFixed(1)} MB`;
}

async function loadArtifacts() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const data = await fetchArtifacts();
    artifacts.value = data.map((item) => ({
      ...item,
      file_size_text: formatFileSize(item.file_size),
      created_at_text: formatDateTime(item.created_at),
    }));
  } catch (error) {
    errorMessage.value = error.message || '读取文件资产失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadArtifacts);
</script>

<template>
  <div class="page-view assets-page">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-card class="page-card assets-hero" :bordered="false">
      <div class="hero-row">
        <div>
          <h3>平台文件资产</h3>
          <p>统一查看模型权重、训练日志、指标文件与报告等平台资产，避免文件散落在不同目录难以追踪。</p>
        </div>
        <t-button theme="primary" :loading="loading" @click="loadArtifacts">刷新资产</t-button>
      </div>
      <div class="hero-metrics">
        <div class="hero-metric"><span>总资产数</span><strong>{{ assetStats.total }}</strong></div>
        <div class="hero-metric"><span>权重文件</span><strong>{{ assetStats.weightCount }}</strong></div>
        <div class="hero-metric"><span>报告文件</span><strong>{{ assetStats.reportCount }}</strong></div>
      </div>
    </t-card>
    <t-card class="page-card translucent-card" title="资产清单">
      <t-table row-key="id" :data="artifacts" :columns="columns" :hover="true" :loading="loading" />
    </t-card>
  </div>
</template>

<style scoped lang="scss">
.assets-page {
  gap: 18px;
}

.assets-hero {
  padding: 20px;
  background:
    radial-gradient(circle at 90% 10%, rgba(59, 130, 246, 0.18), transparent 28%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(239, 246, 255, 0.92));
}

.hero-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.hero-row h3 {
  margin: 0 0 6px;
  font-size: 22px;
}

.hero-row p {
  margin: 0;
  color: var(--app-text-sub);
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.hero-metric {
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid var(--app-border);
  border-radius: 12px;
}

.hero-metric span {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--app-text-sub);
}

.hero-metric strong {
  font-size: 20px;
}

.translucent-card {
  background: rgba(255, 255, 255, 0.84);
}
</style>
