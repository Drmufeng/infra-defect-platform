<script setup>
import { computed, onMounted, ref } from 'vue';
import { fetchModels } from '@/api/platform';

const modelList = ref([]);
const loading = ref(false);
const errorMessage = ref('');

const columns = [
  { colKey: 'model_code', title: '模型编码' },
  { colKey: 'name', title: '模型文件' },
  { colKey: 'task_type', title: '任务类型' },
  { colKey: 'model_type', title: '模型类型' },
  { colKey: 'metric_summary', title: '指标摘要' },
  { colKey: 'weight_path', title: '路径' },
  { colKey: 'publish_status', title: '发布状态' },
  { colKey: 'status', title: '状态' },
];

const modelStats = computed(() => {
  const defaultModel = modelList.value.find((item) => item.is_default);
  const publishedCount = modelList.value.filter((item) => item.publish_status === 'published').length;
  return {
    total: modelList.value.length,
    publishedCount,
    defaultModel: defaultModel?.name || '-',
  };
});

async function loadModels() {
  loading.value = true;
  errorMessage.value = '';
  try {
    modelList.value = await fetchModels();
  } catch (error) {
    errorMessage.value = error.message || '读取模型列表失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadModels);
</script>

<template>
  <div class="page-view models-page">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-card class="page-card models-hero" :bordered="false">
      <div class="hero-row">
        <div>
          <h3>模型发布与注册</h3>
          <p>统一查看模型状态、默认模型与发布信息，面向客户端和管理端提供一致的模型来源。</p>
        </div>
        <t-button theme="primary" :loading="loading" @click="loadModels">同步模型</t-button>
      </div>
      <div class="hero-metrics">
        <div class="hero-metric"><span>模型总数</span><strong>{{ modelStats.total }}</strong></div>
        <div class="hero-metric"><span>已发布</span><strong>{{ modelStats.publishedCount }}</strong></div>
        <div class="hero-metric"><span>默认模型</span><strong>{{ modelStats.defaultModel }}</strong></div>
      </div>
    </t-card>

    <t-card class="page-card translucent-card" title="模型列表">
      <template #actions>
        <t-button variant="text" :loading="loading" @click="loadModels">刷新</t-button>
      </template>
      <t-table row-key="id" :data="modelList" :columns="columns" :hover="true" :loading="loading" />
    </t-card>
  </div>
</template>

<style scoped lang="scss">
.models-page {
  gap: 18px;
}

.models-hero {
  padding: 20px;
  background:
    radial-gradient(circle at 85% 15%, rgba(249, 115, 22, 0.16), transparent 28%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(255, 247, 237, 0.92));
}

.hero-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
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
  background: rgba(255, 255, 255, 0.82);
}

@media (max-width: 900px) {
  .hero-row {
    flex-direction: column;
  }

  .hero-metrics {
    grid-template-columns: 1fr;
  }
}
</style>
