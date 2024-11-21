<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<script setup>
import { onBeforeMount } from 'vue'
import NavBar from './components/NavBar.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 앱이 처음 시작될 때만 실행
if (import.meta.env.DEV) {  // 개발 환경에서만 실행
  const isFirstLoad = !sessionStorage.getItem('appInitialized')
  
  if (isFirstLoad) {
    localStorage.clear()  // localStorage 초기화
    sessionStorage.setItem('appInitialized', 'true')
  }
}

onBeforeMount(() => {
  authStore.initializeToken()  // 토큰 초기화만 실행
})
</script>

<style>
body {
  margin: 0;
  font-family: 'Arial', sans-serif;
}
</style>