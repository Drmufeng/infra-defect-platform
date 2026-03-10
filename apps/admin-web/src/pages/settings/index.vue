<script setup>
import { computed, onMounted, ref } from 'vue';
import { fetchSettings } from '@/api/platform';

const settings = ref([]);
const loading = ref(false);
const errorMessage = ref('');

const settingsGroups = computed(() => {
  const trainingKeys = ['default_model_path'];
  const inferenceKeys = ['default_conf_threshold', 'test_images_dir'];
  const systemKeys = ['database_name'];

  const mapItems = (keys) =>
    settings.value
      .filter((item) => keys.includes(item.setting_key))
      .map((item) => [item.setting_key, item.setting_value]);

  return [
    { title: '训练相关设置', items: mapItems(trainingKeys) },
    { title: '推理相关设置', items: mapItems(inferenceKeys) },
    { title: '系统基础设置', items: mapItems(systemKeys) },
  ];
});

async function loadSettings() {
  loading.value = true;
  errorMessage.value = '';
  try {
    settings.value = await fetchSettings();
  } catch (error) {
    errorMessage.value = error.message || '读取系统设置失败';
  } finally {
    loading.value = false;
  }
}

onMounted(loadSettings);
</script>

<template>
  <div class="page-view">
    <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />
    <t-row :gutter="16">
      <t-col v-for="group in settingsGroups" :key="group.title" :xs="12" :lg="4">
        <t-card class="page-card translucent-card" :title="group.title">
          <template #actions>
            <t-button v-if="group.title === '训练相关设置'" variant="text" :loading="loading" @click="loadSettings">刷新</t-button>
          </template>
          <t-descriptions bordered :column="1">
            <t-descriptions-item v-for="item in group.items" :key="item[0]" :label="item[0]">
              {{ item[1] }}
            </t-descriptions-item>
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
