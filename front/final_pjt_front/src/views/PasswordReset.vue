<template>
  <div class="container mt-5">
    <div class="card p-4">
      <h2 class="mb-4">비밀번호 재설정</h2>
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label class="form-label">새 비밀번호</label>
          <input 
            type="password" 
            class="form-control"
            v-model="formData.new_password1"
            required
          />
        </div>
        <div class="mb-3">
          <label class="form-label">새 비밀번호 확인</label>
          <input 
            type="password" 
            class="form-control"
            v-model="formData.new_password2"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">
          비밀번호 변경
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const formData = ref({
  new_password1: '',
  new_password2: '',
  uid: route.params.uid,
  token: route.params.token
})

const handleSubmit = () => {
  if (formData.value.new_password1 !== formData.value.new_password2) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  axios({
    method: 'post',
    url: '/accounts/password/reset/confirm/',
    data: formData.value
  })
    .then(() => {
      alert('비밀번호가 성공적으로 변경되었습니다.')
      router.push({ name: 'login' })
    })
    .catch((err) => {
      console.error(err)
      alert('비밀번호 변경에 실패했습니다.')
    })
}
</script>