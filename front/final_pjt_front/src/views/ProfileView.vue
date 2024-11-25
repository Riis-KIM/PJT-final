<template>
  <div class="container mt-5">
    <div class="card p-4">
      <h2 class="mb-4">내 정보</h2>
      
      <div v-if="authStore.user">
        <!-- 프로필 보기 모드 -->
        <div v-if="!isEditing && !showPasswordForm">
          <div class="profile-image-section text-center mb-4">
            <div class="profile-image-container">
              <img 
                src="@/assets/images/saessak.png" 
                alt="프로필" 
                class="profile-image"
              />
            </div>
          </div>
          <div class="info-row mb-3">
            <label class="form-label">사용자 이름</label>
            <p class="form-control-static">{{ computedUserInfo.username }}</p>
          </div>

          <div class="info-row mb-3">
            <label class="form-label">이름</label>
            <p class="form-control-static">{{ computedUserInfo.name || '새싹' }}</p>
          </div>

          <div class="info-row mb-3">
            <label class="form-label">이메일</label>
            <p class="form-control-static">{{ computedUserInfo.email || '미설정' }}</p>
          </div>

          <div class="info-row mb-3">
            <label class="form-label">나이</label>
            <p class="form-control-static">{{ computedUserInfo.age || '0' }} 살</p>
          </div>

          <div class="info-row mb-3">
            <label class="form-label">자산</label>
            <p class="form-control-static">{{ computedUserInfo.money || '0' }} 원</p>
          </div>

          <div class="d-grid gap-2">
            <button class="btn btn-primary mb-3" @click="isEditing = true">
              정보 수정하기
            </button>
            <button class="btn btn-secondary" @click="showPasswordForm = true">
              비밀번호 변경
            </button>
          </div>
        </div>

        <!-- 정보 수정 모드 -->
        <div v-if="isEditing">
          <div class="mb-3">
            <label class="form-label">이름</label>
            <input type="text" class="form-control" v-model="editUserInfo.name" />
          </div>

          <div class="mb-3">
            <label class="form-label">이메일</label>
            <input type="email" class="form-control" v-model="editUserInfo.email" />
          </div>

          <div class="mb-3">
            <label class="form-label">나이</label>
            <input type="number" class="form-control" v-model="editUserInfo.age" />
          </div>

          <div class="mb-3">
            <label class="form-label">자산</label>
            <input type="number" class="form-control" v-model="editUserInfo.money" />
          </div>

          <div class="d-grid gap-2">
            <button class="btn btn-success mb-2" @click="saveChanges">
              저장하기
            </button>
            <button class="btn btn-secondary" @click="cancelEdit">
              취소
            </button>
          </div>
        </div>

        <!-- 비밀번호 변경 모드 -->
        <div v-if="showPasswordForm">

          <div class="mb-3">
            <label class="form-label">현재 비밀번호</label>
            <input type="password" class="form-control" v-model="passwordData.old_password" />
          </div>

          <div class="mb-3">
            <label class="form-label">새 비밀번호</label>
            <input type="password" class="form-control" v-model="passwordData.new_password1" />
          </div>

          <div class="mb-3">
            <label class="form-label">새 비밀번호 확인</label>
            <input type="password" class="form-control" v-model="passwordData.new_password2" />
          </div>

          <div class="d-grid gap-2">
            <button class="btn btn-success" @click="handlePasswordChange">
              변경하기
            </button>
            <button class="btn btn-secondary" @click="cancelPasswordChange">
              취소
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const isEditing = ref(false)
const showPasswordForm = ref(false)

// 현재 사용자 정보를 computed로 관리
const computedUserInfo = computed(() => authStore.user || {})

// 수정용 사용자 정보
const editUserInfo = ref({})

// 비밀번호 변경 데이터
const passwordData = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})

// 수정 모드 시작 시 현재 정보 복사
const startEdit = () => {
  editUserInfo.value = { ...computedUserInfo.value }
  isEditing.value = true
}

// 변경사항 저장
const saveChanges = async () => {
  await authStore.updateUserInfo(editUserInfo.value)
  isEditing.value = false
}

// 수정 취소
const cancelEdit = () => {
  editUserInfo.value = { ...computedUserInfo.value }
  isEditing.value = false
}

// 비밀번호 변경 처리
const handlePasswordChange = () => {
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
      cancelPasswordChange()
    })
    .catch((err) => {
      console.error(err)
      alert('비밀번호 변경에 실패했습니다.')
    })
}

// 비밀번호 변경 취소
const cancelPasswordChange = () => {
  passwordData.value = {
    old_password: '',
    new_password1: '',
    new_password2: ''
  }
  showPasswordForm.value = false
}
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.info-row {
  border-bottom: 1px solid #eee;
  padding: 8px 0;
}

.form-control-static {
  margin-bottom: 0;
  padding: 7px 0;
}

.profile-image-container {
  width: 150px;
  height: 150px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #f8f9fa;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.profile-image {
  width: 90%;
  height: 90%;
  object-fit: cover;
}
</style>