<script setup>
import { computed, onMounted, ref } from 'vue';
import { fetchModels, fetchTestingTasks } from '@/api/platform';

const models = ref([]);
const testingTasks = ref([]);
const loading = ref(false);
const errorMessage = ref('');

const latestTask = computed(() => testingTasks.value[0] || null);
const testSamples = computed(() =>
  (latestTask.value?.results || []).map((item) => ({
    image: item.image_name,
    result: `检测到 ${item.detected_count} 处裂缝`,
    confidence: latestTask.value?.conf_threshold ?? '-',
    note: item.summary_json || '已生成结果图',
  })),
);

const columns = [
  { colKey: 'image', title: '图片' },
  { colKey: 'result', title: '检测结果' },
  { colKey: 'confidence', title: '置信度' },
  { colKey: 'note', title: '备注' },
];

async function loadTestingPage() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const [modelData, testingData] = await Promise.all([fetchModels(), fetchTestingTasks()]);
    models.value = modelData;
    testingTasks.value = testingData;
  } catch (error) {
    errorMessage.value = error.message || '读取测试数据失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadTestingPage);
</script>

<template>
  <div class="page-view testing-page">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-card class="page-card testing-hero" :bordered="false">
      <div class="testing-hero__title">
        <h3>推理测试与结果验证</h3>
        <p>选择模型后对测试样本执行推理，重点关注漏检、误检和结果可解释性。</p>
      </div>
      <t-space>
        <t-tag theme="primary" variant="light">任务数 {{ testingTasks.length }}</t-tag>
        <t-tag theme="success" variant="light">当前模型 {{ models.find((item) => item.is_default)?.name || '-' }}</t-tag>
      </t-space>
    </t-card>

    <t-row :gutter="16">
      <t-col :xs="12" :lg="4">
        <t-card class="page-card translucent-card" title="推理测试面板">
          <template #actions>
            <t-button variant="text" :loading="loading" @click="loadTestingPage">刷新</t-button>
          </template>
          <t-form layout="vertical">
            <t-form-item label="模型版本">
              <t-select :value="models.find((item) => item.is_default)?.name || models[0]?.name">
                <t-option v-for="item in models" :key="item.id" :value="item.name" :label="item.name" />
              </t-select>
            </t-form-item>
            <t-form-item label="测试来源目录">
              <t-input :value="latestTask?.input_path || '-'" />
            </t-form-item>
            <t-form-item label="置信度阈值">
              <t-input-number :min="0" :max="1" :step="0.01" :value="latestTask?.conf_threshold || 0.46" />
            </t-form-item>
            <t-space>
              <t-button theme="primary">开始测试</t-button>
              <t-button variant="outline">打开结果目录</t-button>
            </t-space>
          </t-form>
        </t-card>
      </t-col>

      <t-col :xs="12" :lg="8">
        <t-card class="page-card translucent-card" title="最近测试结果">
          <t-table row-key="image" :data="testSamples" :columns="columns" :hover="true" :loading="loading" />
        </t-card>
      </t-col>
    </t-row>
  </div>
</template>

<style scoped lang="scss">
.testing-page {
  gap: 18px;
}

.testing-hero {
  padding: 18px 20px;
  background:
    radial-gradient(circle at 85% 20%, rgba(16, 185, 129, 0.16), transparent 30%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(240, 253, 247, 0.92));
}

.testing-hero__title {
  margin-bottom: 10px;
}

.testing-hero__title h3 {
  margin: 0 0 6px;
  font-size: 22px;
}

.testing-hero__title p {
  margin: 0;
  color: var(--app-text-sub);
}

.translucent-card {
  background: rgba(255, 255, 255, 0.82);
}
</style>
