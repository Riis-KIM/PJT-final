<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import NavBar from './components/NavBar.vue';
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
authStore.initializeToken()
</script>

<style>
body {
  margin: 0;
  font-family: 'Arial', sans-serif;
}
</style>
