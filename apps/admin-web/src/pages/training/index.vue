<script setup>
import { computed, onMounted, ref } from 'vue';
import { fetchDatasets, fetchTrainingJobs } from '@/api/platform';
import { formatMetricSummary } from '@/shared/utils/formatters';

const datasets = ref([]);
const trainingJobs = ref([]);
const loading = ref(false);
const errorMessage = ref('');

const latestJob = computed(() => trainingJobs.value[0] || null);

async function loadTrainingPage() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const [datasetData, trainingData] = await Promise.all([fetchDatasets(), fetchTrainingJobs()]);
    datasets.value = datasetData;
    trainingJobs.value = trainingData;
  } catch (error) {
    errorMessage.value = error.message || '读取训练数据失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadTrainingPage);
</script>

<template>
  <div class="page-view">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-row :gutter="16">
      <t-col :xs="12" :lg="5">
        <t-card class="page-card translucent-card" title="启动训练">
          <template #actions>
            <t-button variant="text" :loading="loading" @click="loadTrainingPage">刷新</t-button>
          </template>
          <t-form layout="vertical">
            <t-form-item label="训练数据集">
              <t-select :value="datasets[0]?.name">
                <t-option v-for="item in datasets" :key="item.id" :value="item.name" :label="item.name" />
              </t-select>
            </t-form-item>
            <t-form-item label="模型权重">
              <t-input :value="latestJob?.base_weight || 'yolov8s.pt'" />
            </t-form-item>
            <t-form-item label="训练轮数">
              <t-input-number :min="1" :value="latestJob?.epochs || 50" />
            </t-form-item>
            <t-form-item label="批大小">
              <t-input-number :min="1" :value="latestJob?.batch_size || 16" />
            </t-form-item>
            <t-form-item label="图像尺寸">
              <t-input-number :min="320" :step="32" :value="latestJob?.image_size || 640" />
            </t-form-item>
            <t-space>
              <t-button theme="primary">启动训练</t-button>
              <t-button variant="outline">查看日志</t-button>
            </t-space>
          </t-form>
        </t-card>
      </t-col>

      <t-col :xs="12" :lg="7">
        <t-card class="page-card translucent-card" title="训练运行信息">
          <t-descriptions bordered :column="1">
            <t-descriptions-item label="当前训练状态">{{ latestJob?.status || '-' }}</t-descriptions-item>
            <t-descriptions-item label="最近训练任务">{{ latestJob?.job_name || '-' }}</t-descriptions-item>
            <t-descriptions-item label="设备">{{ latestJob?.device || '-' }}</t-descriptions-item>
            <t-descriptions-item label="轮数">{{ latestJob?.epochs || '-' }}</t-descriptions-item>
            <t-descriptions-item label="关键指标">{{ formatMetricSummary(latestJob?.metric) }}</t-descriptions-item>
            <t-descriptions-item label="结果目录">{{ latestJob?.output_dir || '-' }}</t-descriptions-item>
          </t-descriptions>
        </t-card>
      </t-col>
    </t-row>
  </div>
</template>

<style scoped lang="scss">
.translucent-card {
  background: rgba(255, 255, 255, 0.82);
}
</style>
