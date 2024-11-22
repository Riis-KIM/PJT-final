<template>
  <div>
    <nav class="navbar navbar-expand-lg">
      <div class="container">
        <!-- 로고 -->
        <router-link to="/" class="navbar-brand d-flex align-items-center">
          <img src="@/assets/images/logo.webp" alt="로고" class="logo-image me-2" />
          <span class="brand-name">Seedly</span>
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
              <router-link to="/recommendations" class="nav-link">금융상품추천</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/rates" class="nav-link">금리비교</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/exchange" class="nav-link">환율계산기</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/map" class="nav-link">은행지도</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/community" class="nav-link">커뮤니티</router-link>
            </li>
          </ul>

          <!-- 오른쪽 메뉴 -->
          <div class="d-flex align-items-center">
            <router-link to="/profile" class="me-3 text-dark">
              <i class="bi bi-person fs-5"></i>
            </router-link>
            <router-link to="/cart" class="me-3 text-dark">
              <i class="bi bi-cart fs-5"></i>
            </router-link>
            <button class="btn btn-outline-primary ms-3" @click="handleAuth">
              {{ isLoggedIn ? "로그아웃" : "로그인" }}
            </button>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const router = useRouter();
const authStore = useAuthStore();

// computed 속성으로 로그인 상태 관리
const isLoggedIn = computed(() => authStore.isAuthenticated);

const handleAuth = () => {
  if (isLoggedIn.value) {
    authStore.logout();
  } else {
    router.push({ name: "login" });
  }
};
</script>

<style scoped>
/* 네비게이션 바 스타일 */
.navbar {
  background-color: white;
  border-bottom: 2px solid #ddd;
  padding: 1rem 0;
  font-family: "Arial", sans-serif;
}

/* 로고 이미지 */
.logo-image {
  height: 50px;
  width: auto;
}

.brand-name {
  font-weight: bold;
  font-size: 1.5rem;
  color: #333;
}

/* 중앙 메뉴 스타일 */
.nav-link {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin: 0 1rem;
  text-transform: uppercase;
  transition: color 0.3s ease-in-out;
}

.nav-link:hover {
  color: #007bff;
  text-decoration: underline;
}

/* 오른쪽 아이콘 스타일 */
.bi {
  font-size: 1.5rem;
  color: #555;
  cursor: pointer;
}

.bi:hover {
  color: #007bff;
}

.btn-outline-primary {
  font-weight: 600;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=UTF8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3E%3Cpath stroke='rgba%280,0,0,0.7%29' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}
</style>
