<template>
  <div class="container mt-5">
    <!-- 로그인 여부에 따라 다른 내용 표시 -->
    <div v-if="authStore.isAuthenticated">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold">커뮤니티</h2>
        <button 
          class="btn btn-link fw-bold" 
          @click="goToCreateArticle"
        >
          글쓰기
        </button>
      </div>

      <!-- 게시글 목록 -->
      <div>
        <div class="border-bottom pb-3 mb-3" v-for="article in articleStore.articles" :key="article.id">
          <h5 
            class="fw-bold mb-2" 
            @click="goToDetail(article.id)" 
            style="cursor: pointer"
          >
            {{ article.title }}
          </h5>
          <p class="text-muted small mb-1">
            작성자: {{ article.username }}
          </p>
          <p class="text-muted small">
            댓글 {{ article.comment_count }}개 | {{ formatDate(article.created_at) }}
          </p>
        </div>
      </div>
    </div>

    <!-- 비로그인 상태일 때 메시지 표시 -->
    <div v-else class="text-center mt-5">
      <p class="fw-bold text-muted mb-4">로그인 없이는 커뮤니티를 볼 수 없습니다.</p>
      <button class="btn btn-link fw-bold" @click="goToLogin">
        로그인 페이지로 이동
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const articleStore = useArticleStore()
const authStore = useAuthStore()

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR')
}

// 게시글 작성 페이지로 이동
const goToCreateArticle = () => {
  router.push({ name: 'articleCreate' })
}

// 게시글 상세 페이지로 이동
const goToDetail = (articleId) => {
  router.push({ 
    name: 'articleDetail', 
    params: { id: articleId }
  })
}

// 로그인 페이지로 이동
const goToLogin = () => {
  router.push({ name: 'login' })
}

// 컴포넌트 마운트 시 게시글 목록 가져오기
onMounted(() => {
  if (authStore.isAuthenticated) {
    articleStore.getArticles()
  }
})
</script>

<style scoped>
/* 전체 배경을 흰색으로 통일 */
.container {
  background-color: #fff;
  color: #000;
}

/* 제목 스타일 */
h2 {
  font-size: 1.5rem;
}

/* 게시글 제목 클릭 시 스타일 */
h5 {
  font-size: 1.2rem;
  color: #000;
  margin-bottom: 0.5rem;
}

h5:hover {
  text-decoration: underline;
}

/* 작성자 및 댓글 정보 텍스트 */
.text-muted {
  font-size: 0.9rem;
}

/* 버튼 스타일 */
.btn-link {
  text-decoration: none;
  color: #000;
}

.btn-link:hover {
  text-decoration: underline;
}

/* 게시글 구분선 */
.border-bottom {
  border-color: #ddd;
}
</style>
