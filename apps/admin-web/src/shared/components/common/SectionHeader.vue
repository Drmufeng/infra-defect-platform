<script setup>
defineProps({
  title: String,
  description: String,
});
</script>

<template>
  <div class="section-header">
    <div>
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
    </div>
    <div class="section-header__actions">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.section-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.section-header h3 {
  margin: 0;
  font-size: 22px;
}

.section-header p {
  margin: 6px 0 0;
  color: var(--app-text-sub);
}

.section-header__actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
  }
}
</style>
