<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>커뮤니티</h2>
      <button 
        v-if="authStore.isAuthenticated"
        class="btn btn-primary" 
        @click="goToCreateArticle"
      >
        글쓰기
      </button>
    </div>

    <!-- 게시글 목록 -->
    <div class="card mb-3" v-for="article in articleStore.articles" :key="article.id">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="card-title" @click="goToDetail(article.id)" style="cursor: pointer">
            {{ article.title }}
          </h5>
          <small class="text-muted">{{ article.username }}</small>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-2">
          <small class="text-muted">
            댓글 {{ article.comment_count }}개
          </small>
          <small class="text-muted">
            {{ formatDate(article.created_at) }}
          </small>
        </div>
      </div>
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

// 날짜 포맷팅
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

// 컴포넌트 마운트 시 게시글 목록 가져오기
onMounted(() => {
  articleStore.getArticles()
})
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-title {
  margin-bottom: 0;
}

.card-title:hover {
  color: #007bff;
}
</style>