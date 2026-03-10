<script setup>
defineProps({
  title: String,
  subtitle: String,
  status: String,
  description: String,
  metrics: {
    type: Array,
    default: () => [],
  },
  actions: {
    type: Array,
    default: () => [],
  },
});
</script>

<template>
  <t-card class="page-card feature-card" :bordered="false">
    <div class="feature-card__top">
      <div>
        <div class="feature-card__subtitle">{{ subtitle }}</div>
        <h4>{{ title }}</h4>
      </div>
      <t-tag theme="primary" variant="light">{{ status }}</t-tag>
    </div>

    <p class="feature-card__desc">{{ description }}</p>

    <div class="feature-card__metrics">
      <div v-for="item in metrics" :key="item.label" class="feature-card__metric">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
      </div>
    </div>

    <div class="feature-card__actions">
      <t-button
        v-for="action in actions"
        :key="action.label"
        :theme="action.theme || 'default'"
        :variant="action.variant || 'outline'"
      >
        {{ action.label }}
      </t-button>
    </div>
  </t-card>
</template>

<style scoped lang="scss">
.feature-card {
  height: 100%;
  background: rgba(255, 255, 255, 0.88);
}

.feature-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.feature-card__subtitle {
  color: var(--app-brand);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.feature-card h4 {
  margin: 8px 0 0;
  font-size: 20px;
}

.feature-card__desc {
  min-height: 48px;
  margin: 16px 0;
  color: var(--app-text-sub);
  line-height: 1.7;
}

.feature-card__metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.feature-card__metric {
  padding: 12px;
  background: rgba(15, 23, 42, 0.03);
  border-radius: 14px;
}

.feature-card__metric span {
  display: block;
  margin-bottom: 6px;
  color: var(--app-text-sub);
  font-size: 12px;
}

.feature-card__metric strong {
  font-size: 18px;
}

.feature-card__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
