<template>
  <div class="container mt-5">
    <div class="card p-4">
      <h2 class="mb-4">내 정보</h2>
      
      <div v-if="authStore.user">
        <div class="mb-3">
          <label class="form-label">사용자 이름</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="userInfo.username" 
            readonly
          />
        </div>

        <div class="mb-3">
          <label class="form-label">이름</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="userInfo.name"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">이메일</label>
          <input 
            type="email" 
            class="form-control" 
            v-model="userInfo.email"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">나이</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="userInfo.age"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">자산</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="userInfo.money"
          />
        </div>

        <div class="d-grid gap-2">
          <button 
            class="btn btn-primary" 
            @click="updateProfile"
          >
            정보 수정
          </button>
        </div>
      </div>
      
      <div v-else>
        <p>사용자 정보를 불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const userInfo = ref({
  username: '',
  name: '',
  email: '',
  age: 0,
  money: 0
})

// authStore.user가 변경될 때마다 userInfo 업데이트
watch(() => authStore.user, (newUser) => {
  if (newUser) {
    userInfo.value = { ...newUser }
  }
}, { immediate: true })

// 사용자 정보 가져오기
const getUserInfo = () => {
  authStore.fetchUserInfo()
}

onMounted(() => {
  if (authStore.token) {
    getUserInfo()
  }
})

// 프로필 업데이트
const updateProfile = () => {
  authStore.updateUserInfo(userInfo.value)
}
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.form-control:read-only {
  background-color: #f8f9fa;
}
</style>