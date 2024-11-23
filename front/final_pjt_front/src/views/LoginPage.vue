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
      
      <div class="text-center mt-3">
        <button 
          class="btn btn-link"
          @click="showResetForm = true"
        >
          비밀번호를 잊으셨나요?
        </button>
      </div>
      
      <p class="text-center mt-2">
        계정이 없으신가요? <router-link to="/register">회원가입</router-link>
      </p>
    </form>

    <!-- 비밀번호 초기화 모달 -->
    <div v-if="showResetForm" class="modal-backdrop">
      <div class="modal-content">
        <h3>비밀번호 초기화</h3>
        <p>가입한 이메일 주소를 입력하시면 비밀번호 재설정 링크를 보내드립니다.</p>
        <div class="mb-3">
          <input 
            type="email" 
            class="form-control"
            v-model="resetEmail"
            placeholder="이메일 주소"
          />
        </div>
        <div class="d-flex gap-2">
          <button 
            class="btn btn-primary"
            @click="handlePasswordReset"
          >
            재설정 링크 받기
          </button>
          <button 
            class="btn btn-secondary"
            @click="showResetForm = false"
          >
            취소
          </button>
        </div>
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
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.btn-link {
  padding: 0;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}

.gap-2 {
  gap: 0.5rem;
}
</style>