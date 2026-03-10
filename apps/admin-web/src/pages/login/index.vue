<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '@/api/platform';
import { setAuthSession } from '@/shared/utils/auth';

const router = useRouter();
const submitting = ref(false);
const errorMessage = ref('');
const form = ref({
  username: 'admin',
  password: '1234',
});

async function handleLogin() {
  submitting.value = true;
  errorMessage.value = '';
  try {
    const result = await login(form.value);
    setAuthSession({ accessToken: result.access_token, user: result.user });
    router.replace('/dashboard');
  } catch (error) {
    errorMessage.value = error.message || '登录失败';
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <div class="login-shell">
    <div class="login-panel">
      <div class="login-header">
        <p class="eyebrow">Admin Login</p>
        <h1>基础设施病害管理端</h1>
        <p>使用后台账号登录后，可查看模型资产、审计日志与训练测试状态。</p>
      </div>

      <t-alert v-if="errorMessage" theme="error" :message="errorMessage" />

      <t-form layout="vertical">
        <t-form-item label="用户名">
          <t-input v-model="form.username" />
        </t-form-item>
        <t-form-item label="密码">
          <t-input v-model="form.password" type="password" />
        </t-form-item>
        <t-button theme="primary" block :loading="submitting" @click="handleLogin">登录管理端</t-button>
      </t-form>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-shell {
  display: grid;
  min-height: 100vh;
  place-items: center;
  padding: 20px;
  background:
    radial-gradient(circle at top right, rgba(14, 165, 233, 0.18), transparent 28%),
    linear-gradient(160deg, rgba(239, 246, 255, 1), rgba(248, 250, 252, 1));
}

.login-panel {
  width: min(460px, 100%);
  padding: 28px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--app-border);
  border-radius: 24px;
  box-shadow: var(--app-shadow);
}

.login-header {
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--app-brand);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.login-header h1 {
  margin: 0 0 8px;
  font-size: 28px;
}

.login-header p {
  margin: 0;
  color: var(--app-text-sub);
}
</style>
