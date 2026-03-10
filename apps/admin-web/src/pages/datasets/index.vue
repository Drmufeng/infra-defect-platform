<script setup>
import { computed, onMounted, ref } from 'vue';
import { fetchDatasets } from '@/api/platform';

const datasets = ref([]);
const loading = ref(false);
const errorMessage = ref('');

const columns = [
  { colKey: 'name', title: '数据集名称' },
  { colKey: 'version', title: '版本' },
  { colKey: 'source_type', title: '来源' },
  { colKey: 'label_strategy', title: '标签策略' },
  { colKey: 'train_count', title: '训练集' },
  { colKey: 'val_count', title: '验证集' },
  { colKey: 'status', title: '状态' },
];

const datasetStats = computed(() => {
  const totalTrain = datasets.value.reduce((sum, item) => sum + (item.train_count || 0), 0);
  const totalVal = datasets.value.reduce((sum, item) => sum + (item.val_count || 0), 0);
  const latest = datasets.value[0];
  return {
    versionCount: datasets.value.length,
    totalSamples: totalTrain + totalVal,
    latestVersion: latest?.version || '-',
    latestStatus: latest?.status || '-',
  };
});

async function loadDatasets() {
  loading.value = true;
  errorMessage.value = '';
  try {
    datasets.value = await fetchDatasets();
  } catch (error) {
    errorMessage.value = error.message || '读取数据集失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadDatasets);
</script>

<template>
  <div class="page-view dataset-page">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-card class="page-card dataset-hero" :bordered="false">
      <div class="hero-top">
        <div>
          <h3>数据集资产中心</h3>
          <p>统一管理数据集版本、标签策略与样本规模，为训练与推理提供稳定输入。</p>
        </div>
        <t-button theme="primary" :loading="loading" @click="loadDatasets">同步数据</t-button>
      </div>
      <t-row :gutter="12">
        <t-col :xs="12" :sm="6">
          <div class="hero-stat"><span>数据集版本</span><strong>{{ datasetStats.versionCount }}</strong></div>
        </t-col>
        <t-col :xs="12" :sm="6">
          <div class="hero-stat"><span>总样本数</span><strong>{{ datasetStats.totalSamples }}</strong></div>
        </t-col>
        <t-col :xs="12" :sm="6">
          <div class="hero-stat"><span>最新版本</span><strong>{{ datasetStats.latestVersion }}</strong></div>
        </t-col>
        <t-col :xs="12" :sm="6">
          <div class="hero-stat"><span>最新状态</span><strong>{{ datasetStats.latestStatus }}</strong></div>
        </t-col>
      </t-row>
    </t-card>

    <t-row :gutter="16">
      <t-col :xs="12" :lg="8">
        <t-card class="page-card translucent-card" title="数据集版本列表">
          <template #actions>
            <t-button variant="text" :loading="loading" @click="loadDatasets">刷新</t-button>
          </template>
          <t-table row-key="id" :data="datasets" :columns="columns" :hover="true" :loading="loading" />
        </t-card>
      </t-col>
      <t-col :xs="12" :lg="4">
        <t-card class="page-card translucent-card" title="数据导入">
          <t-form layout="vertical">
            <t-form-item label="导入来源">
              <t-select placeholder="请选择导入方式">
                <t-option value="zip" label="导入原始压缩包" />
                <t-option value="dir" label="导入本地目录" />
                <t-option value="xml" label="导入标注目录" />
              </t-select>
            </t-form-item>
            <t-form-item label="目标版本号">
              <t-input placeholder="例如 v2" />
            </t-form-item>
            <t-form-item label="标签策略">
              <t-select placeholder="请选择标签策略">
                <t-option value="crack_only" label="单类别 crack" />
                <t-option value="official4" label="官方四分类" />
              </t-select>
            </t-form-item>
            <t-space>
              <t-button theme="primary">开始导入</t-button>
              <t-button variant="outline">执行预处理</t-button>
            </t-space>
          </t-form>
        </t-card>
      </t-col>
    </t-row>
  </div>
</template>

<style scoped lang="scss">
.dataset-page {
  gap: 18px;
}

.dataset-hero {
  padding: 20px;
  background:
    radial-gradient(circle at 90% 10%, rgba(20, 116, 234, 0.16), transparent 30%),
    linear-gradient(140deg, rgba(255, 255, 255, 0.96), rgba(242, 248, 255, 0.92));
}

.hero-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.hero-top h3 {
  margin: 0 0 6px;
  font-size: 22px;
}

.hero-top p {
  margin: 0;
  color: var(--app-text-sub);
}

.hero-stat {
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid var(--app-border);
  border-radius: 12px;
}

.hero-stat span {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--app-text-sub);
}

.hero-stat strong {
  font-size: 20px;
}

.translucent-card {
  background: rgba(255, 255, 255, 0.82);
}
</style>
