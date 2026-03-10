<script setup>
import { computed, onMounted, ref } from 'vue';
import FeatureCard from '@/shared/components/common/FeatureCard.vue';
import SectionHeader from '@/shared/components/common/SectionHeader.vue';
import StatCard from '@/shared/components/common/StatCard.vue';
import { fetchDatasets, fetchModels, fetchOverview, fetchRuntimeStatus, fetchTestingTasks, fetchTrainingJobs } from '@/api/platform';
import { formatDateTime, formatMetricSummary } from '@/shared/utils/formatters';

const loading = ref(false);
const errorMessage = ref('');
const overview = ref(null);
const runtimeStatus = ref(null);
const datasets = ref([]);
const models = ref([]);
const trainingJobs = ref([]);
const testingTasks = ref([]);

const columns = [
  { colKey: 'name', title: '训练任务' },
  { colKey: 'status', title: '状态' },
  { colKey: 'epochs', title: '轮数' },
  { colKey: 'device', title: '设备' },
  { colKey: 'duration', title: '时间' },
  { colKey: 'metric', title: '关键指标' },
];

const sampleColumns = [
  { colKey: 'image', title: '测试图片' },
  { colKey: 'result', title: '检测结果' },
  { colKey: 'confidence', title: '阈值' },
  { colKey: 'note', title: '备注' },
];

const runtimeColumns = [
  { colKey: 'label', title: '检查项' },
  { colKey: 'path', title: '路径' },
  { colKey: 'status', title: '状态' },
];

const overviewStats = computed(() => {
  const totalTrain = datasets.value.reduce((sum, item) => sum + (item.train_count || 0), 0);
  const totalVal = datasets.value.reduce((sum, item) => sum + (item.val_count || 0), 0);
  const defaultModel = models.value.find((item) => item.is_default);
  const latestJob = trainingJobs.value[0];

  return [
    { title: '数据集版本', value: String(overview.value?.dataset_count || 0), trend: '当前启用 v1', theme: 'primary' },
    { title: '训练样本数', value: String(totalTrain + totalVal), trend: `train ${totalTrain} / val ${totalVal}`, theme: 'success' },
    { title: '当前默认模型', value: defaultModel?.name || '-', trend: defaultModel ? '已写入数据库' : '待初始化', theme: 'warning' },
    { title: '测试任务数', value: String(overview.value?.inference_task_count || 0), trend: latestJob ? latestJob.status : '暂无任务', theme: 'danger' },
  ];
});

const dashboardCards = computed(() => {
  const activeDataset = datasets.value[0];
  const latestJob = trainingJobs.value[0];
  const defaultModel = models.value.find((item) => item.is_default) || models.value[0];
  const latestTesting = testingTasks.value[0];

  return [
    {
      id: 'datasets',
      title: '数据集管理',
      subtitle: 'Dataset Center',
      status: activeDataset?.status || '待导入',
      description: '统一查看原始数据、处理后数据集、标签策略与数据导入状态，为训练版本管理提供基础支撑。',
      metrics: [
        { label: '当前版本', value: activeDataset?.version || '-' },
        { label: '训练 / 验证', value: `${activeDataset?.train_count || 0} / ${activeDataset?.val_count || 0}` },
        { label: '标签策略', value: activeDataset?.label_strategy || '-' },
        { label: '原始来源', value: activeDataset?.source_type || '-' },
      ],
      actions: [
        { label: '查看数据集', theme: 'primary', variant: 'base' },
        { label: '导入数据' },
      ],
    },
    {
      id: 'training',
      title: '模型训练',
      subtitle: 'Training Jobs',
      status: latestJob?.status || '待启动',
      description: '从后台统一发起训练、查看训练日志和关键指标，并对不同模型版本进行横向对比。',
      metrics: [
        { label: '训练轮数', value: latestJob?.epochs || '-' },
        { label: '批大小', value: latestJob?.batch_size || '-' },
        { label: '默认权重', value: latestJob?.base_weight || '-' },
        { label: '设备', value: latestJob?.device || '-' },
      ],
      actions: [
        { label: '启动训练', theme: 'primary', variant: 'base' },
        { label: '查看日志' },
      ],
    },
    {
      id: 'models',
      title: '模型管理',
      subtitle: 'Model Registry',
      status: defaultModel?.is_default ? '默认模型' : '可切换',
      description: '集中管理 best.pt、last.pt 与后续导出模型，支持标记默认模型和查看关键评估指标。',
      metrics: [
        { label: '默认模型', value: defaultModel?.name || '-' },
        { label: '任务类型', value: defaultModel?.task_type || '-' },
        { label: '状态', value: defaultModel?.status || '-' },
        { label: '路径', value: defaultModel?.weight_path?.split('/').slice(-2).join('/') || '-' },
      ],
      actions: [
        { label: '查看模型', theme: 'primary', variant: 'base' },
        { label: '切换默认' },
      ],
    },
    {
      id: 'testing',
      title: '推理测试',
      subtitle: 'Inference Lab',
      status: latestTesting?.status || '待测试',
      description: '对独立测试图片执行批量推理，观察误检、漏检、框贴合情况，并为后端接口联调准备测试样例。',
      metrics: [
        { label: '测试目录', value: overview.value?.test_images_dir?.split('/').slice(-1)[0] || '-' },
        { label: '阈值', value: latestTesting?.conf_threshold ?? '-' },
        { label: '样例数量', value: latestTesting?.results?.length || 0 },
        { label: '结果目录', value: latestTesting?.output_path?.split('/').slice(-1)[0] || '-' },
      ],
      actions: [
        { label: '开始测试', theme: 'primary', variant: 'base' },
        { label: '查看结果' },
      ],
    },
  ];
});

const trainingRuns = computed(() =>
  trainingJobs.value.map((item) => ({
    name: item.job_name,
    status: item.status,
    epochs: `${item.epochs}`,
    device: item.device,
    duration: item.finished_at ? formatDateTime(item.finished_at) : formatDateTime(item.created_at),
    metric: formatMetricSummary(item.metric),
  })),
);

const testSamples = computed(() => {
  const latestTask = testingTasks.value[0];
  if (!latestTask) {
    return [];
  }

  return (latestTask.results || []).map((item) => ({
    image: item.image_name,
    result: `检测到 ${item.detected_count} 处裂缝`,
    confidence: latestTask.conf_threshold ?? '-',
    note: item.summary_json || '已写入测试结果',
  }));
});

const runtimeRows = computed(() =>
  (runtimeStatus.value?.paths || []).map((item) => ({
    label: item.label,
    path: item.path,
    status: item.exists ? '可用' : '缺失',
  })),
);

const runtimeSummary = computed(() => {
  if (!runtimeStatus.value) {
    return '-';
  }
  const availableCount = (runtimeStatus.value.paths || []).filter((item) => item.exists).length;
  return `${availableCount}/${runtimeStatus.value.paths.length} 可用`;
});

async function loadPageData() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const [overviewData, runtimeData, datasetData, trainingData, modelData, testingData] = await Promise.all([
      fetchOverview(),
      fetchRuntimeStatus(),
      fetchDatasets(),
      fetchTrainingJobs(),
      fetchModels(),
      fetchTestingTasks(),
    ]);
    overview.value = overviewData;
    runtimeStatus.value = runtimeData;
    datasets.value = datasetData;
    trainingJobs.value = trainingData;
    models.value = modelData;
    testingTasks.value = testingData;
  } catch (error) {
    errorMessage.value = error.message || '加载页面数据失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadPageData);
</script>

<template>
  <div class="page-view card-list-page">
    <div class="card-list-hero">
      <SectionHeader
        title="基础设施病害平台能力总览"
        description="首页已接入 FastAPI 后端概览、数据集、训练、模型和测试接口，用于展示平台当前真实状态。"
      >
        <t-button theme="primary" :loading="loading" @click="loadPageData">刷新数据</t-button>
        <t-button variant="outline">查看文档</t-button>
      </SectionHeader>
      <t-alert v-if="errorMessage" theme="error" :message="errorMessage" close />
    </div>

    <t-row :gutter="16">
      <t-col v-for="item in overviewStats" :key="item.title" :xs="12" :sm="6" :lg="3">
        <StatCard v-bind="item" />
      </t-col>
    </t-row>

    <SectionHeader
      title="核心模块"
      description="每张卡片均来自真实后端数据，可作为后续功能扩展和联调入口。"
    />

    <t-row :gutter="16">
      <t-col v-for="card in dashboardCards" :key="card.id" :xs="12" :md="6" :xl="3">
        <FeatureCard v-bind="card" />
      </t-col>
    </t-row>

    <t-row :gutter="16">
      <t-col :xs="12" :lg="7">
        <t-card class="page-card translucent-card" :bordered="false">
          <template #header>
            <SectionHeader title="最近训练记录" description="当前表格直接读取训练任务与训练指标接口。">
              <t-button variant="text" @click="loadPageData">重新读取</t-button>
            </SectionHeader>
          </template>
          <t-table row-key="name" :data="trainingRuns" :columns="columns" :hover="true" />
        </t-card>
      </t-col>
      <t-col :xs="12" :lg="5">
        <t-card class="page-card translucent-card" :bordered="false">
          <template #header>
            <SectionHeader title="运行时状态" description="新增后端 runtime 接口，前端可快速定位路径和环境问题。">
              <t-button variant="text" @click="loadPageData">重新检查</t-button>
            </SectionHeader>
          </template>
          <t-space direction="vertical" style="width: 100%">
            <t-tag theme="primary" variant="light">
              服务状态 {{ runtimeStatus?.health || '-' }} / 目录检查 {{ runtimeSummary }}
            </t-tag>
            <t-tag theme="success" variant="light">服务器时间 {{ formatDateTime(runtimeStatus?.server_time) }}</t-tag>
            <t-table row-key="path" size="small" :data="runtimeRows" :columns="runtimeColumns" :hover="true" />
          </t-space>
        </t-card>
      </t-col>
    </t-row>

    <t-card class="page-card translucent-card" :bordered="false">
      <template #header>
        <SectionHeader title="最近测试样例" description="当前样例来自后端测试任务与结果记录。">
          <t-tag theme="success" variant="light">manual 测试集</t-tag>
        </SectionHeader>
      </template>
      <t-table row-key="image" :data="testSamples" :columns="sampleColumns" :hover="true" />
    </t-card>
  </div>
</template>

<style scoped lang="scss">
.card-list-page {
  gap: 20px;
}

.card-list-hero {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px 26px;
  background:
    radial-gradient(circle at top right, rgba(0, 82, 217, 0.14), transparent 26%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(245, 248, 255, 0.92));
  border: 1px solid var(--app-border);
  border-radius: 24px;
  box-shadow: var(--app-shadow);
}

.translucent-card {
  background: rgba(255, 255, 255, 0.84);
}
</style>
