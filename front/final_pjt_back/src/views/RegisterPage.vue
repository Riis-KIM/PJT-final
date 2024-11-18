<template>
  <div class="register-container">
    <h2 class="text-center">회원가입</h2>
    <form @submit.prevent="handleRegister">
      <!-- 사용자명 입력 -->
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

      <!-- 이름 입력 -->
      <div class="mb-3">
        <label for="name" class="form-label">이름</label>
        <input
          type="text"
          class="form-control"
          id="name"
          v-model="formData.name"
          placeholder="이름을 입력하세요"
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

      <!-- 나이 입력 -->
      <div class="mb-3">
        <label for="age" class="form-label">나이</label>
        <input
          type="number"
          class="form-control"
          id="age"
          v-model="formData.age"
          placeholder="나이를 입력하세요"
        />
      </div>

      <!-- 초기 자산 입력 -->
      <div class="mb-3">
        <label for="money" class="form-label">초기 자산</label>
        <input
          type="number"
          class="form-control"
          id="money"
          v-model="formData.money"
          placeholder="초기 자산을 입력하세요"
        />
      </div>

      <!-- 회원가입 버튼 -->
      <button type="submit" class="btn btn-primary w-100">회원가입</button>
    </form>

    <!-- 로그인 링크 -->
    <p class="text-center mt-3">
      이미 계정이 있으신가요? <router-link to="/login">로그인</router-link>
    </p>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'

export default {
  name: "RegisterPage",
  setup() {
    const authStore = useAuthStore()
    
    const formData = ref({
      username: '',
      name: '',
      email: '',
      password: '',
      age: null,
      money: null
    })

    const handleRegister = async () => {
      // 필드 검증
      if (!formData.value.username || !formData.value.password) {
        alert("필수 항목을 모두 입력하세요.");
        return;
      }

      // 비밀번호 유효성 검사
      if (formData.value.password.length < 6) {
        alert("비밀번호는 최소 6자 이상이어야 합니다.");
        return;
      }

      try {
        await authStore.register(formData.value)
      } catch (error) {
        console.error("회원가입 중 오류 발생:", error)
        alert("회원가입 중 문제가 발생했습니다. 다시 시도해주세요.")
      }
    }

    return {
      formData,
      handleRegister
    }
  }
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