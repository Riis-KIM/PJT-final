<template>
  <div class="login-container">
    <h2 class="text-center">로그인</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="username" class="form-label">사용자명</label>
        <input
          type="text"
          class="form-control"
          id="username"
          v-model="formData.username"
          placeholder="사용자명을 입력하세요"
          required
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="formData.password"
          placeholder="비밀번호를 입력하세요"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary w-100">로그인</button>
      <p class="text-center mt-3">
        계정이 없으신가요? <router-link to="/register">회원가입</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  password: ''
})

const handleLogin = () => {
  if (!formData.value.username || !formData.value.password) {
    alert('사용자명과 비밀번호를 입력해주세요.')
    return
  }

  authStore.login(formData.value)
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
}
</style>