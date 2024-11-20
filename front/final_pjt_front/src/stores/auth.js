// store/auth.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const token = ref(null)
  const user = ref(null)

  const isAuthenticated = computed(() => {
    return token.value !== null
  })

  // 회원가입
  const register = function (payload) {
    axios({
      method: 'post',
      url: '/accounts/signup/',
      data: {
        username: payload.username,
        password1: payload.password1,
        password2: payload.password2,
        email: payload.email
      }
    })
      .then(() => {
        router.push({ name: 'login' })
      })
      .catch((err) => {
        console.error(err)
        if (err.response?.data) {
          // Django에서 보내는 에러 메시지 표시
          const errorMessage = Object.values(err.response.data).flat().join('\n')
          alert(errorMessage)
        } else {
          alert('회원가입 중 오류가 발생했습니다.')
        }
      })
  }

  // 로그인
  const login = function (payload) {
    axios({
      method: 'post',
      url: '/accounts/login/',
      data: {
        username: payload.username,
        password: payload.password
      }
    })
      .then((res) => {
        token.value = res.data.key
        localStorage.setItem('token', res.data.key)
        router.push({ name: 'home' })
      })
      .catch((err) => {
        console.error(err)
        alert('로그인에 실패했습니다.')
      })
  }

  // 로그아웃
  const logout = function () {
    axios({
      method: 'post',
      url: '/accounts/logout/',
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        token.value = null
        localStorage.removeItem('token')
        router.push({ name: 'login' })
      })
      .catch((err) => {
        console.error(err)
      })
  }

  // 토큰 초기화
  const initializeToken = function () {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      token.value = storedToken
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    register,
    login,
    logout,
    initializeToken,
  }
}, {
  persist: {
    paths: ['token', 'user']
  }
})