<script setup>
defineProps({
  title: String,
  value: String,
  trend: String,
  theme: String,
});
</script>

<template>
  <t-card class="page-card stat-card" :bordered="false">
    <div class="stat-card__title">{{ title }}</div>
    <div class="stat-card__value">{{ value }}</div>
    <t-tag :theme="theme || 'primary'" variant="light">{{ trend }}</t-tag>
  </t-card>
</template>

<style scoped lang="scss">
.stat-card {
  min-height: 148px;
  background: rgba(255, 255, 255, 0.82);
}

.stat-card__title {
  margin-bottom: 14px;
  color: var(--app-text-sub);
}

.stat-card__value {
  margin-bottom: 16px;
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}
</style>
