<template>
  <div>
    <nav class="navbar navbar-expand-lg">
      <div class="container">
        
        <!-- 로고 -->
        <router-link to="/" class="navbar-brand d-flex align-items-center">
          <img src="@/assets/images/download-rewmrkrf378uz87tgbc53ehj4e-removebg-preview.png" alt="로고" class="logo-image me-3" />
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
            <li class="nav-item nav-map">
              <router-link to="/map" class="nav-link btn-hover-effect">은행지도</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/community" class="nav-link">커뮤니티</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'chatbot' }" class="nav-link">챗봇</router-link>
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
            <button class="btn btn-outline-primary ms-3 btn-hover-effect" @click="handleAuth">
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
  height: 70px; /* 로고 크기 증가 */
  width: auto;
  margin-right: 1rem; /* 메뉴와 간격 조정 */
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
  color: #28a745; /* 초록색으로 변경 */
  text-decoration: underline;
}

/* 오른쪽 아이콘 스타일 */
.bi {
  font-size: 1.5rem;
  color: #555;
  cursor: pointer;
}

.bi:hover {
  color: #28a745; /* 초록색으로 변경 */
}

.btn-outline-primary {
  font-weight: 600;
  position: relative;
  z-index: 1; /* 나뭇잎 효과 위에 글씨 */
  overflow: hidden; /* 배경 이미지가 버튼 안에만 표시되도록 */
  border-color: #28a745; /* 초록색 테두리 */
  color: #28a745; /* 초록색 텍스트 */
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: #28a745; /* 초록색 배경 */
  color: white;
}

.btn-hover-effect::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("/src/assets/images/Lovepik_com-401343102-leaves.png");
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0;
  z-index: -1; /* 버튼 텍스트 아래 */
  transition: opacity 0.3s ease;
}

.btn-hover-effect:hover::after {
  opacity: 0.4; /* 나뭇잎 투명도 조정 */
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=UTF8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3E%3Cpath stroke='rgba%280,128,0,0.7%29' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E"); /* 초록색 토글 아이콘 */
}

/* 은행지도 링크에 나뭇잎 효과 추가 */
.nav-map .btn-hover-effect {
  position: relative;
  z-index: 1; /* 나뭇잎 효과 위에 글씨 */
  overflow: hidden; /* 나뭇잎 배경이 링크 안에만 표시되도록 */
  color: #333; /* 기본 텍스트 색상 */
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-map .btn-hover-effect::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("/src/assets/images/Lovepik_com-401343102-leaves.png"); /* 나뭇잎 배경 */
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0;
  z-index: -1; /* 텍스트 아래에 배치 */
  transition: opacity 0.3s ease;
}

.nav-map .btn-hover-effect:hover {
  color: #28a745; /* 호버 시 텍스트 색상 변경 */
  background-color: white; /* 초록색 배경 추가 */
}

.nav-map .btn-hover-effect:hover::after {
  opacity: 0.4; /* 나뭇잎 배경 투명도 조정 */
}
</style>
