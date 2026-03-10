<script setup>
import { onMounted, ref } from 'vue';
import { fetchClientProfile, submitClientReport } from '@/api/platform';
import { formatDateTime } from '@/shared/utils/formatters';

const loading = ref(false);
const submitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const modelList = ref([]);
const profile = ref(null);

const form = ref({
  client_name: 'desktop_client',
  model_id: '',
  run_id: '',
  input_path: '',
  output_path: '',
  report_path: '',
  conf_threshold: '',
  summary_json: '',
});

const columns = [
  { colKey: 'name', title: '模型文件' },
  { colKey: 'model_code', title: '模型编码' },
  { colKey: 'model_type', title: '类型' },
  { colKey: 'weight_path', title: '权重路径' },
  { colKey: 'metric_summary', title: '指标摘要' },
  { colKey: 'status', title: '状态' },
  { colKey: 'publish_status', title: '发布状态' },
  { colKey: 'is_default', title: '默认' },
];

async function loadClientProfile() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const data = await fetchClientProfile();
    profile.value = data;
    modelList.value = data.models || [];
    if (!form.value.model_id && data.default_model_id) {
      form.value.model_id = String(data.default_model_id);
    }
    if (!form.value.conf_threshold) {
      form.value.conf_threshold = String(data.default_conf_threshold ?? '0.46');
    }
  } catch (error) {
    errorMessage.value = error.message || '读取客户端接入配置失败';
  } finally {
    loading.value = false;
  }
}

async function handleSubmitReport() {
  if (!form.value.client_name.trim()) {
    errorMessage.value = '请先输入客户端名称';
    return;
  }
  submitting.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  try {
    const payload = {
      client_name: form.value.client_name.trim(),
      model_id: form.value.model_id ? Number(form.value.model_id) : null,
      run_id: form.value.run_id.trim() || null,
      input_path: form.value.input_path.trim() || null,
      output_path: form.value.output_path.trim() || null,
      report_path: form.value.report_path.trim() || null,
      conf_threshold: form.value.conf_threshold ? Number(form.value.conf_threshold) : null,
      summary_json: form.value.summary_json.trim() || null,
    };
    const result = await submitClientReport(payload);
    successMessage.value = `回传成功，任务ID ${result.task_id}，运行ID ${result.run_id}`;
    form.value.run_id = '';
    form.value.summary_json = '';
  } catch (error) {
    errorMessage.value = error.message || '回传客户端报告失败';
  } finally {
    submitting.value = false;
  }
}

onMounted(loadClientProfile);
</script>

<template>
  <div class="page-view client-access-page">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-alert v-if="successMessage" theme="success" :message="successMessage" />
    <t-card class="page-card client-access-hero" :bordered="false">
      <div class="hero-header">
        <div>
          <h3>客户端接入管理</h3>
          <p>统一管理客户端可见模型、默认阈值与本地推理结果回传协议，确保管理端与客户端使用同一套模型资产。</p>
        </div>
        <t-button theme="primary" :loading="loading" @click="loadClientProfile">同步接入配置</t-button>
      </div>
      <div class="hero-tags">
        <t-tag theme="primary" variant="light">默认阈值 {{ profile?.default_conf_threshold ?? '-' }}</t-tag>
        <t-tag theme="success" variant="light">默认模型 {{ profile?.default_model_id ?? '-' }}</t-tag>
        <t-tag theme="warning" variant="light">模型数量 {{ modelList.length }}</t-tag>
      </div>
    </t-card>

    <t-row :gutter="16">
      <t-col :xs="12" :lg="4">
        <t-card class="page-card translucent-card" title="客户端报告回传">
          <t-form layout="vertical">
            <t-form-item label="客户端名称">
              <t-input v-model="form.client_name" placeholder="例如 desktop_client" />
            </t-form-item>
            <t-form-item label="模型ID">
              <t-select v-model="form.model_id" placeholder="默认使用平台默认模型">
                <t-option v-for="item in modelList" :key="item.id" :value="String(item.id)" :label="`${item.id} - ${item.name}`" />
              </t-select>
            </t-form-item>
            <t-form-item label="运行ID（可选）">
              <t-input v-model="form.run_id" placeholder="不填则后端自动生成" />
            </t-form-item>
            <t-form-item label="输入路径"><t-input v-model="form.input_path" /></t-form-item>
            <t-form-item label="输出路径"><t-input v-model="form.output_path" /></t-form-item>
            <t-form-item label="报告路径"><t-input v-model="form.report_path" /></t-form-item>
            <t-form-item label="置信度阈值"><t-input v-model="form.conf_threshold" /></t-form-item>
            <t-form-item label="摘要JSON"><t-textarea v-model="form.summary_json" :autosize="{ minRows: 3, maxRows: 6 }" /></t-form-item>
            <t-space>
              <t-button theme="primary" :loading="submitting" @click="handleSubmitReport">回传结果</t-button>
              <t-button variant="outline" @click="loadClientProfile">刷新配置</t-button>
            </t-space>
          </t-form>
        </t-card>
      </t-col>
      <t-col :xs="12" :lg="8">
        <t-card class="page-card translucent-card" title="客户端可用模型清单">
          <template #actions>
            <t-tag theme="primary" variant="light">默认阈值 {{ profile?.default_conf_threshold ?? '-' }}</t-tag>
          </template>
          <t-table row-key="id" :data="modelList" :columns="columns" :hover="true" :loading="loading" />
        </t-card>
        <t-card class="page-card translucent-card top-gap" title="客户端默认测试目录">
          <t-descriptions bordered :column="1">
            <t-descriptions-item label="test_images_dir">{{ profile?.test_images_dir || '-' }}</t-descriptions-item>
            <t-descriptions-item label="默认模型ID">{{ profile?.default_model_id || '-' }}</t-descriptions-item>
            <t-descriptions-item label="配置读取时间">{{ formatDateTime(new Date()) }}</t-descriptions-item>
          </t-descriptions>
        </t-card>
      </t-col>
    </t-row>
  </div>
</template>

<style scoped lang="scss">
.client-access-page {
  gap: 18px;
}

.client-access-hero {
  padding: 20px;
  background:
    radial-gradient(circle at 90% 10%, rgba(14, 165, 233, 0.16), transparent 28%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(240, 249, 255, 0.92));
}

.hero-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 12px;
}

.hero-header h3 {
  margin: 0 0 6px;
  font-size: 22px;
}

.hero-header p {
  margin: 0;
  color: var(--app-text-sub);
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.translucent-card {
  background: rgba(255, 255, 255, 0.82);
}

.top-gap {
  margin-top: 16px;
}

@media (max-width: 900px) {
  .hero-header {
    flex-direction: column;
  }
}
</style>
