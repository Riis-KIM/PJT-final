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
            class="btn btn-primary mb-3" 
            @click="updateProfile"
          >
            정보 수정
          </button>
          <button 
            class="btn btn-secondary" 
            @click="showPasswordForm = !showPasswordForm"
          >
            비밀번호 변경
          </button>
        </div>

        <!-- 비밀번호 변경 폼 -->
        <div v-if="showPasswordForm" class="mt-4 border-top pt-4">
          <h3 class="mb-3">비밀번호 변경</h3>
          <div class="mb-3">
            <label class="form-label">현재 비밀번호</label>
            <input 
              type="password" 
              class="form-control"
              v-model="passwordData.old_password"
            />
          </div>
          <div class="mb-3">
            <label class="form-label">새 비밀번호</label>
            <input 
              type="password" 
              class="form-control"
              v-model="passwordData.new_password1"
            />
          </div>
          <div class="mb-3">
            <label class="form-label">새 비밀번호 확인</label>
            <input 
              type="password" 
              class="form-control"
              v-model="passwordData.new_password2"
            />
          </div>
          <button 
            class="btn btn-primary"
            @click="changePassword"
          >
            비밀번호 변경
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
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const userInfo = ref({
  username: '',
  name: '',
  email: '',
  age: 0,
  money: 0
})

const showPasswordForm = ref(false)
const passwordData = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})

watch(() => authStore.user, (newUser) => {
  if (newUser) {
    userInfo.value = { ...newUser }
  }
}, { immediate: true })

const getUserInfo = () => {
  authStore.fetchUserInfo()
}

const updateProfile = () => {
  authStore.updateUserInfo(userInfo.value)
}

const changePassword = () => {
  if (passwordData.value.new_password1 !== passwordData.value.new_password2) {
    alert('새 비밀번호가 일치하지 않습니다')
    return
  }

  axios({
    method: 'post',
    url: '/accounts/password/change/',
    data: passwordData.value,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then(() => {
      alert('비밀번호가 성공적으로 변경되었습니다.')
      passwordData.value = {
        old_password: '',
        new_password1: '',
        new_password2: ''
      }
      showPasswordForm.value = false
    })
    .catch((err) => {
      console.error(err)
      alert('비밀번호 변경에 실패했습니다.')
    })
}

onMounted(() => {
  if (authStore.token) {
    getUserInfo()
  }
})
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