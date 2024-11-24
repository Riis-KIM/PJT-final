<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="text-center mb-4">로그인</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">사용자명</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-person"></i></span>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="formData.username"
              placeholder="사용자명을 입력하세요"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">비밀번호</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-lock"></i></span>
            <input
              :type="showPassword ? 'text' : 'password'"
              class="form-control"
              id="password"
              v-model="formData.password"
              placeholder="비밀번호를 입력하세요"
              required
            />
            <button class="btn btn-outline-secondary" type="button" @click="togglePassword">
              <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
        </div>

        <button type="submit" class="btn btn-primary w-100 mt-3">로그인</button>
      </form>

      <div class="text-center mt-3">
        <button class="btn btn-link" @click="showResetForm = true">
          비밀번호를 잊으셨나요?
        </button>
      </div>

      <p class="text-center mt-3">
        계정이 없으신가요? <router-link to="/register" class="text-primary">회원가입</router-link>
      </p>
    </div>
  </div>

    <!-- 비밀번호 초기화 모달 -->
  <div v-if="showResetForm" class="modal-backdrop" @click.self="showResetForm = false">
    <div class="modal-content">
      <h3 class="mb-3">비밀번호 초기화</h3>
      <p>가입한 이메일 주소를 입력하시면 비밀번호 재설정 링크를 보내드립니다.</p>
      <div class="mb-3">
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-envelope"></i></span>
          <input 
            type="email" 
            class="form-control"
            v-model="resetEmail"
            placeholder="이메일 주소"
          />
        </div>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-primary flex-grow-1" @click="handlePasswordReset">
          재설정 링크 받기
        </button>
        <button class="btn btn-secondary" @click="showResetForm = false">
          취소
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const showResetForm = ref(false)
const resetEmail = ref('')
const showPassword = ref(false)

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

const handlePasswordReset = () => {
  if (!resetEmail.value) {
    alert('이메일을 입력해주세요.')
    return
  }
  
  authStore.resetPassword(resetEmail.value)
  showResetForm.value = false
  resetEmail.value = ''
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600;700&display=swap');
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

body {
  font-family: 'Roboto', 'Open Sans', sans-serif;
  background-color: #f8f9fa;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

h2, h3 {
  color: #343a40;
  font-weight: 600;
}

.form-label {
  font-weight: 500;
  color: #495057;
}

.input-group-text {
  background-color: #f8f9fa;
  border-right: none;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  box-shadow: none;
  border-color: #ced4da;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-link {
  color: #007bff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.btn-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  max-width: 400px;
  width: 90%;
}

.text-primary {
  color: #007bff !important;
}

.gap-2 {
  gap: 0.5rem;
}
</style>