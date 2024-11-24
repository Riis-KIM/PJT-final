<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="text-center mb-4">회원가입</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="username" class="form-label">사용자 이름</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-person"></i></span>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="formData.username"
              placeholder="사용자 이름을 입력하세요"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">이메일</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-envelope"></i></span>
            <input
              type="email"
              class="form-control"
              id="email"
              v-model="formData.email"
              placeholder="이메일을 입력하세요"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label for="password1" class="form-label">비밀번호</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-lock"></i></span>
            <input
              type="password"
              class="form-control"
              id="password1"
              v-model="formData.password1"
              placeholder="비밀번호를 입력하세요"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label for="password2" class="form-label">비밀번호 확인</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
            <input
              type="password"
              class="form-control"
              id="password2"
              v-model="formData.password2"
              placeholder="비밀번호를 다시 입력하세요"
              required
            />
          </div>
        </div>

        <button type="submit" class="btn btn-primary w-100 mt-3">회원가입</button>
      </form>

      <p class="text-center mt-3">
        이미 계정이 있으신가요? <router-link to="/login" class="text-primary">로그인</router-link>
      </p>
    </div>
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
  email: '',
  password1: '',
  password2: ''
})

const handleRegister = () => {
  if (formData.value.password1 !== formData.value.password2) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  if (formData.value.password1.length < 8) {
    alert('비밀번호는 8자 이상이어야 합니다.')
    return
  }

  authStore.register(formData.value)
    .then(() => {
      router.push('/dashboard')
    })
    .catch((error) => {
      alert('회원가입 중 오류가 발생했습니다: ' + error.message)
    })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css');

body {
  font-family: 'Roboto', 'Open Sans', sans-serif;
  background-color: #f8f9fa;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.register-card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

h2 {
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

.text-primary {
  color: #007bff !important;
  text-decoration: none;
  transition: color 0.3s ease;
}

.text-primary:hover {
  color: #0056b3 !important;
  text-decoration: underline;
}
</style>