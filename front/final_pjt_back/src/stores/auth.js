// stores/auth.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://localhost:8000/api/v1'
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
      url: `${API_URL}/register/`,
      data: {
        username: payload.username,
        name: payload.name,
        email: payload.email,
        password: payload.password,
        age: payload.age,
        money: payload.money
      }
    })
      .then((res) => {
        // console.log(res)
        // // 회원가입 성공 시 자동 로그인
        // login({
        //   username: payload.username,
        //   password: payload.password
        // })
        router.push({name:'login'})
      })
      .catch((err) => {
        if (err.response?.status === 400) {
          window.alert('이미 존재하는 회원입니다.')
        } else {
          console.log(err)
        }
      })
  }

  // 로그인
  const login = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/login/`,
      data: {
        username: payload.username,
        password: payload.password
      }
    })
      .then((res) => {
        token.value = res.data.token
        user.value = res.data.user
        localStorage.setItem('token', res.data.token)
      })
      .then(() => {
        router.push({ name: 'home' })
      })
      .catch((err) => {
        window.alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.')
      })
  }

  // 로그아웃
  const logout = function () {
    axios({
      method: 'post',
      url: `${API_URL}/logout/`,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
      .then(() => {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        window.alert('로그아웃되었습니다.')
      })
      .then(() => {
        router.push({ name: 'login' })
      })
      .catch((err) => {
        console.error(err)
      })
  }

  // 사용자 프로필 조회
  const getProfile = function () {
    axios({
      method: 'get',
      url: `${API_URL}/profile/`,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
      .then((res) => {
        user.value = res.data
      })
      .catch((err) => {
        console.error(err)
      })
  }

  // 프로필 업데이트
  const updateProfile = function (payload) {
    axios({
      method: 'put',
      url: `${API_URL}/profile/update/`,
      data: payload,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
      .then((res) => {
        user.value = res.data
        window.alert('프로필이 업데이트되었습니다.')
      })
      .catch((err) => {
        console.error(err)
      })
  }

  return {
    API_URL,
    user,
    token,
    isAuthenticated,
    register,
    login,
    logout,
    getProfile,
    updateProfile
  }
}, {
  persist: {
    paths: ['token', 'user']
  }
})