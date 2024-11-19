<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
      <div class="container">
        <!-- 로고 -->
        <router-link to="/" class="navbar-brand">
          <img src="@/assets/images/logo.webp" alt="로고" class="logo-image" />
        </router-link>

        <!-- 모바일 토글 버튼 -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- 네비게이션 메뉴 -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav mx-auto">
            <li class="nav-item">
              <router-link to="/rates" class="nav-link fw-bold">금리비교</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/exchange" class="nav-link fw-bold">환율계산기</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/map" class="nav-link fw-bold">은행지도</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/community" class="nav-link fw-bold">커뮤니티</router-link>
            </li>
          </ul>

          <!-- 오른쪽 아이콘 -->
          <div class="d-flex align-items-center">
            <router-link to="/search" class="me-3 text-dark">
              <i class="bi bi-search fs-5"></i>
            </router-link>
            <router-link to="/favorites" class="me-3 text-dark">
              <i class="bi bi-heart fs-5"></i>
            </router-link>
            <router-link to="/cart" class="me-3 text-dark">
              <i class="bi bi-cart fs-5"></i>
            </router-link>

            <!-- 로그인/로그아웃 버튼 -->
            <button
              class="btn btn-outline-primary ms-3"
              @click="handleAuth"
            >
              {{ isLoggedIn ? "로그아웃" : "로그인" }}
            </button>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>


<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

// computed 속성으로 로그인 상태 관리
const isLoggedIn = computed(() => authStore.isAuthenticated)

const handleAuth = () => {
  if (isLoggedIn.value) {
    // 로그아웃 처리
    authStore.logout()
  } else {
    // 로그인 페이지로 이동만 수행
    router.push({ name: 'login' })
  }
}
</script>

<style scoped>
/* 로고 이미지 스타일 */
.logo-image {
  height: 50px; /* 로고 높이 조정 */
  width: auto;  /* 가로 비율 유지 */
}

/* 반응형 크기 조정 */
@media (max-width: 768px) {
  .logo-image {
    height: 40px; /* 모바일 화면에서 로고 크기 축소 */
  }
}

@media (max-width: 576px) {
  .logo-image {
    height: 30px; /* 더 작은 화면에서는 로고를 더 축소 */
  }
}
</style>
