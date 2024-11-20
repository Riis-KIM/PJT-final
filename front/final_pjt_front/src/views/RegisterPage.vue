<template>
  <div class="register-container">
    <h2 class="text-center">회원가입</h2>
    <form @submit.prevent="handleRegister">
      <!-- 사용자명 입력 -->
      <div class="mb-3">
        <label for="username" class="form-label">사용자 이름</label>
        <input
          type="text"
          class="form-control"
          id="username"
          v-model="formData.username"
          placeholder="사용자 이름을 입력하세요"
          required
        />
      </div>

      <!-- 이메일 입력 -->
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <input
          type="email"
          class="form-control"
          id="email"
          v-model="formData.email"
          placeholder="이메일을 입력하세요"
          required
        />
      </div>

      <!-- 비밀번호 입력 -->
      <div class="mb-3">
        <label for="password1" class="form-label">비밀번호</label>
        <input
          type="password"
          class="form-control"
          id="password1"
          v-model="formData.password1"
          placeholder="비밀번호를 입력하세요"
          required
        />
      </div>

      <!-- 비밀번호 확인 -->
      <div class="mb-3">
        <label for="password2" class="form-label">비밀번호 확인</label>
        <input
          type="password"
          class="form-control"
          id="password2"
          v-model="formData.password2"
          placeholder="비밀번호를 다시 입력하세요"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary w-100">회원가입</button>
    </form>

    <p class="text-center mt-3">
      계정이 있으신가요? <router-link to="/login">로그인</router-link>
    </p>
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
  // 비밀번호 확인
  if (formData.value.password1 !== formData.value.password2) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  // 비밀번호 길이 검증
  if (formData.value.password1.length < 8) {
    alert('비밀번호는 8자 이상이어야 합니다.')
    return
  }

  authStore.register(formData.value)
}
</script>

<style scoped>
.register-container {
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

.form-control {
  margin-bottom: 10px;
}

.btn-primary {
  margin-top: 10px;
}
</style>