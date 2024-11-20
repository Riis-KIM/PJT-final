<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-body">
        <h2 class="card-title mb-4">
          {{ isEditing ? '게시글 수정' : '새 게시글 작성' }}
        </h2>

        <form @submit.prevent="submitArticle">
          <!-- 제목 입력 -->
          <div class="mb-3">
            <label for="title" class="form-label">제목</label>
            <input 
              type="text" 
              class="form-control" 
              id="title"
              v-model="articleData.title"
              placeholder="제목을 입력하세요"
              required
            >
          </div>

          <!-- 내용 입력 -->
          <div class="mb-3">
            <label for="content" class="form-label">내용</label>
            <textarea 
              class="form-control" 
              id="content"
              v-model="articleData.content"
              rows="10"
              placeholder="내용을 입력하세요"
              required
            ></textarea>
          </div>

          <!-- 버튼 그룹 -->
          <div class="d-flex gap-2">
            <button 
              type="submit" 
              class="btn btn-primary"
            >
              {{ isEditing ? '수정' : '작성' }}
            </button>
            <button 
              type="button" 
              class="btn btn-secondary"
              @click="goBack"
            >
              취소
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'

const route = useRoute()
const router = useRouter()
const articleStore = useArticleStore()

// 수정 모드인지 확인
const isEditing = computed(() => {
  return route.name === 'articleEdit'
})

// 게시글 데이터
const articleData = ref({
  title: '',
  content: ''
})

// 수정 모드일 경우 기존 데이터 불러오기
onMounted(() => {
  if (isEditing.value) {
    articleStore.getArticle(route.params.id)
      .then(() => {
        articleData.value = {
          title: articleStore.article.title,
          content: articleStore.article.content
        }
      })
  }
})

// 게시글 제출 (작성 또는 수정)
const submitArticle = () => {
  if (!articleData.value.title.trim() || !articleData.value.content.trim()) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  if (isEditing.value) {
    articleStore.updateArticle(route.params.id, articleData.value)
      .then(() => {
        router.push({
          name: 'articleDetail',
          params: { id: route.params.id }
        })
      })
  } else {
    articleStore.createArticle(articleData.value)
      .then(() => {
        router.push({ name: 'community' })
      })
  }
}

// 이전 페이지로 돌아가기
const goBack = () => {
  router.back()
}
</script>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

textarea {
  resize: vertical;
  min-height: 200px;
}
</style>