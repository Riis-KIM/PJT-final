<template>
  <div class="community-container">
    <div v-if="authStore.isAuthenticated" class="content-wrapper">
      <div class="header-section">
        <h2 class="page-title">커뮤니티</h2>
        <button 
          class="btn-create"
          @click="goToCreateArticle"
        >
          <i class="bi bi-plus-circle"></i> 글쓰기
        </button>
      </div>

      <div class="article-list">
        <div 
          v-for="article in articleStore.articles" 
          :key="article.id"
          class="article-item"
          @click="goToDetail(article.id)"
        >
          <h3 class="article-title">{{ article.title }}</h3>
          <div class="article-meta">
            <!-- 작성자 -->
            <span class="author">
              <i class="bi bi-person"></i> {{ article.username }}
            </span>
            <!-- 댓글 수 -->
            <span class="comments">
              <i class="bi bi-chat"></i> {{ article.comment_count }}
            </span>
            <!-- 조회수 -->
            <span class="views">
              <i class="bi bi-eye"></i> 조회수: {{ article.views || 0 }}
            </span>
            <!-- 좋아요 수 -->
            <span class="likes">
              <i class="bi bi-hand-thumbs-up"></i> 추천: {{ article.like_count || 0 }}
            </span>
            <!-- 작성일 -->
            <span class="date">
              <i class="bi bi-calendar"></i> {{ formatDate(article.created_at) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="login-prompt">
      <i class="bi bi-lock large-icon"></i>
      <p class="prompt-message">로그인이 필요한 서비스입니다</p>
      <button class="btn-login" @click="goToLogin">
        로그인 하러 가기
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

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' })
}

const goToCreateArticle = () => {
  router.push({ name: 'articleCreate' })
}

const goToDetail = (articleId) => {
  router.push({ 
    name: 'articleDetail', 
    params: { id: articleId }
  })
}

const goToLogin = () => {
  router.push({ name: 'login' })
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    articleStore.getArticles()
  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.community-container {
  font-family: 'Noto Sans KR', sans-serif;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f8f9f9; /* 연한 초록 배경 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #28a745; /* 진한 초록색 제목 */
}

.btn-create {
  position: relative;
  background-color: white;
  color: #28a745;
  border: 1px solid #28a745;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  overflow: hidden;
  transition: background-color 0.3s ease, color 0.3s ease;
  z-index: 1; /* 나뭇잎 효과 위에 글씨 */
  overflow: hidden; /* 나뭇잎 배경이 링크 안에만 표시되도록 */
}

.btn-create::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/images/Lovepik_com-401343102-leaves.png");
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0;
  z-index: -1;
  transition: opacity 0.3s ease;
}

.btn-create:hover {
  color: white;
  background-color: #28a745;
}

.btn-create:hover::after {
  opacity: 0.4;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.article-item {
  padding: 1rem;
  border-radius: 8px;
  background-color: #e9f7ef; /* 밝은 초록 배경 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.article-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.article-title {
  font-size: 1.2rem;
  font-weight: 500;
  color: #333; /* 원래 진회색 */
  margin-bottom: 0.5rem;
}

.article-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #6c757d;
}

.article-meta .views, 
.article-meta .likes {
  font-size: 0.9rem;
}

.login-prompt {
  text-align: center;
  padding: 3rem;
}

.large-icon {
  font-size: 3rem;
  color: #28a745; /* 초록 아이콘 */
  margin-bottom: 1rem;
}

.prompt-message {
  font-size: 1.2rem;
  color: #28a745; /* 초록 메시지 */
  margin-bottom: 1.5rem;
}

.btn-login {
  background-color: #28a745; /* 초록색 버튼 */
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.btn-login:hover {
  background-color: #218838; /* 어두운 초록색 호버 */
}

</style>
