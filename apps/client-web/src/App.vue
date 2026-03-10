<script setup>
import { computed, onMounted, ref } from 'vue';
import { fetchClientProfile, submitClientReport } from './api/client';

const loading = ref(false);
const submitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const profile = ref(null);

const form = ref({
  client_name: 'desktop_client',
  model_id: '',
  run_id: '',
  input_path: '',
  output_path: '',
  report_path: '',
  conf_threshold: '',
  summary_json: '{"risk":"medium","message":"客户端本地检测已完成"}',
});

const modelOptions = computed(() => profile.value?.models || []);

const profileStats = computed(() => [
  { label: '默认模型 ID', value: profile.value?.default_model_id || '-' },
  { label: '默认阈值', value: profile.value?.default_conf_threshold || '-' },
  { label: '模型数量', value: modelOptions.value.length },
]);

async function loadProfile() {
  loading.value = true;
  errorMessage.value = '';
  try {
    const data = await fetchClientProfile();
    profile.value = data;
    if (!form.value.model_id && data.default_model_id) {
      form.value.model_id = String(data.default_model_id);
    }
    if (!form.value.conf_threshold) {
      form.value.conf_threshold = String(data.default_conf_threshold || 0.46);
    }
  } catch (error) {
    errorMessage.value = error.message || '读取客户端配置失败';
  } finally {
    loading.value = false;
  }
}

async function handleSubmit() {
  submitting.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  try {
    const result = await submitClientReport({
      client_name: form.value.client_name.trim(),
      model_id: form.value.model_id ? Number(form.value.model_id) : null,
      run_id: form.value.run_id.trim() || null,
      input_path: form.value.input_path.trim() || null,
      output_path: form.value.output_path.trim() || null,
      report_path: form.value.report_path.trim() || null,
      conf_threshold: form.value.conf_threshold ? Number(form.value.conf_threshold) : null,
      summary_json: form.value.summary_json.trim() || null,
    });
    successMessage.value = `回传成功：任务 ${result.task_id} / 运行 ${result.run_id}`;
    form.value.run_id = '';
  } catch (error) {
    errorMessage.value = error.message || '回传失败';
  } finally {
    submitting.value = false;
  }
}

onMounted(loadProfile);
</script>

<template>
  <main class="client-shell">
    <section class="hero-card">
      <div>
        <p class="eyebrow">Client Web</p>
        <h1>基础设施病害检测客户端</h1>
        <p class="hero-desc">客户端本地完成模型推理，平台负责下发模型配置并归档运行结果与报告。</p>
      </div>
      <div class="hero-actions">
        <button class="primary-btn" :disabled="loading" @click="loadProfile">{{ loading ? '读取中...' : '同步接入配置' }}</button>
      </div>
    </section>

    <section class="stats-grid">
      <article v-for="item in profileStats" :key="item.label" class="stat-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
      </article>
    </section>

    <section class="content-grid">
      <article class="panel-card form-card">
        <div class="panel-header">
          <div>
            <h2>结果回传</h2>
            <p>填写客户端本地推理后的输出路径、报告路径和摘要信息。</p>
          </div>
        </div>

        <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="message success">{{ successMessage }}</p>

        <div class="field-grid">
          <label>
            <span>客户端名称</span>
            <input v-model="form.client_name" placeholder="desktop_client" />
          </label>
          <label>
            <span>模型 ID</span>
            <select v-model="form.model_id">
              <option value="">默认模型</option>
              <option v-for="model in modelOptions" :key="model.id" :value="String(model.id)">
                {{ model.id }} - {{ model.name }}
              </option>
            </select>
          </label>
          <label>
            <span>运行 ID</span>
            <input v-model="form.run_id" placeholder="可空，后端自动生成" />
          </label>
          <label>
            <span>置信度阈值</span>
            <input v-model="form.conf_threshold" placeholder="0.46" />
          </label>
          <label class="span-2">
            <span>输入路径</span>
            <input v-model="form.input_path" placeholder="D:/inspection/input" />
          </label>
          <label class="span-2">
            <span>输出路径</span>
            <input v-model="form.output_path" placeholder="D:/inspection/output" />
          </label>
          <label class="span-2">
            <span>报告路径</span>
            <input v-model="form.report_path" placeholder="D:/inspection/reports/result.pdf" />
          </label>
          <label class="span-2">
            <span>摘要 JSON</span>
            <textarea v-model="form.summary_json"></textarea>
          </label>
        </div>

        <div class="panel-actions">
          <button class="primary-btn" :disabled="submitting" @click="handleSubmit">{{ submitting ? '回传中...' : '提交结果' }}</button>
        </div>
      </article>

      <article class="panel-card models-card">
        <div class="panel-header">
          <div>
            <h2>可用模型清单</h2>
            <p>后端统一下发已启用模型，客户端按需下载并本地推理。</p>
          </div>
        </div>

        <div v-if="!modelOptions.length" class="empty-state">当前暂无模型可用，请先在管理端完成模型发布。</div>

        <div v-else class="model-list">
          <article v-for="model in modelOptions" :key="model.id" class="model-item">
            <div class="model-top">
              <strong>{{ model.name }}</strong>
              <span :class="['pill', model.is_default ? 'pill-primary' : 'pill-muted']">{{ model.is_default ? '默认模型' : '候选模型' }}</span>
            </div>
            <p>{{ model.metric_summary || '暂无指标摘要' }}</p>
            <dl>
              <div>
                <dt>编码</dt>
                <dd>{{ model.model_code || '-' }}</dd>
              </div>
              <div>
                <dt>类型</dt>
                <dd>{{ model.model_type }}</dd>
              </div>
              <div>
                <dt>状态</dt>
                <dd>{{ model.status }}</dd>
              </div>
              <div class="span-full">
                <dt>权重路径</dt>
                <dd>{{ model.weight_path }}</dd>
              </div>
            </dl>
          </article>
        </div>
      </article>
    </section>
  </main>
</template>

<style scoped>
.client-shell {
  max-width: 1180px;
  margin: 0 auto;
  padding: 32px 18px 48px;
}

.hero-card,
.panel-card,
.stat-card {
  border: 1px solid var(--client-border);
  border-radius: 22px;
  box-shadow: var(--client-shadow);
}

.hero-card {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  padding: 28px;
  background:
    radial-gradient(circle at top right, rgba(14, 165, 233, 0.16), transparent 26%),
    linear-gradient(140deg, rgba(255, 255, 255, 0.96), rgba(240, 253, 250, 0.92));
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--client-primary);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

h1,
h2 {
  margin: 0;
}

.hero-desc,
.panel-header p,
.model-item p,
.empty-state {
  color: var(--client-subtext);
}

.hero-desc {
  max-width: 720px;
  margin-top: 10px;
}

.primary-btn {
  padding: 12px 18px;
  color: #fff;
  background: linear-gradient(135deg, #0284c7, #0f766e);
  border: none;
  border-radius: 12px;
  cursor: pointer;
}

.primary-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 18px;
}

.stat-card {
  padding: 16px 18px;
  background: rgba(255, 255, 255, 0.86);
}

.stat-card span {
  display: block;
  margin-bottom: 8px;
  color: var(--client-subtext);
  font-size: 13px;
}

.stat-card strong {
  font-size: 26px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 16px;
  margin-top: 18px;
}

.panel-card {
  padding: 22px;
  background: rgba(255, 255, 255, 0.88);
}

.panel-header {
  margin-bottom: 16px;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label span,
dt {
  font-size: 13px;
  color: var(--client-subtext);
}

input,
textarea,
select {
  width: 100%;
  padding: 11px 12px;
  color: var(--client-text);
  background: #fff;
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 12px;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

.span-2,
.span-full {
  grid-column: 1 / -1;
}

.panel-actions {
  margin-top: 16px;
}

.message {
  margin: 0 0 14px;
  padding: 10px 12px;
  border-radius: 12px;
}

.message.error {
  color: #991b1b;
  background: rgba(254, 226, 226, 0.9);
}

.message.success {
  color: #065f46;
  background: rgba(209, 250, 229, 0.9);
}

.model-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.model-item {
  padding: 16px;
  background: linear-gradient(180deg, rgba(248, 250, 252, 0.96), rgba(255, 255, 255, 0.92));
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 16px;
}

.model-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.pill {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.pill-primary {
  color: #075985;
  background: rgba(186, 230, 253, 0.9);
}

.pill-muted {
  color: #475569;
  background: rgba(226, 232, 240, 0.9);
}

dl {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin: 12px 0 0;
}

dd {
  margin: 4px 0 0;
  word-break: break-all;
}

@media (max-width: 900px) {
  .hero-card,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .hero-card {
    flex-direction: column;
  }

  .stats-grid,
  .field-grid,
  dl {
    grid-template-columns: 1fr;
  }
}
</style>
