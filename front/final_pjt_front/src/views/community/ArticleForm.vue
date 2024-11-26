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
import { ref, onMounted, computed, watch } from 'vue'
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
  }
})

// watch를 추가하여 article 데이터 변경 감지
watch(() => articleStore.article, (newArticle) => {
  if (newArticle && isEditing.value) {
    articleData.value = {
      title: newArticle.title,
      content: newArticle.content
    }
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
    router.push({
      name: 'articleDetail',
      params: { id: route.params.id }
    })
  } else {
    articleStore.createArticle(articleData.value)
    router.push({ name: 'community' })
  }
}

// 이전 페이지로 돌아가기
const goBack = () => {
  router.back()
}
</script>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #ccc; /* 회색 테두리로 복원 */
  border-radius: 8px;
}

.card-title {
  color: #28a745; /* 초록색 제목 */
  font-weight: bold;
}

textarea {
  resize: vertical;
  min-height: 200px;
  border: 1px solid #ccc; /* 회색 테두리로 복원 */
  border-radius: 5px;
}

textarea:focus {
  outline: none;
  border-color: #218838; /* 더 진한 초록색 포커스 */
  box-shadow: 0 0 5px rgba(40, 167, 69, 0.5); /* 초록색 포커스 효과 */
}

input {
  border: 1px solid #ccc; /* 회색 테두리로 복원 */
  border-radius: 5px;
}

input:focus {
  outline: none;
  border-color: #218838; /* 더 진한 초록색 포커스 */
  box-shadow: 0 0 5px rgba(40, 167, 69, 0.5); /* 초록색 포커스 효과 */
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #28a745; /* 초록색 버튼 */
  border: 1px solid #28a745; /* 초록색 테두리 */
  color: white;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-primary:hover {
  background-color: #218838; /* 더 진한 초록색 호버 */
  border-color: #218838;
}

.btn-secondary {
  background-color: white; /* 흰색 배경 */
  border: 1px solid #28a745; /* 초록색 테두리 */
  color: #28a745; /* 초록색 텍스트 */
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-secondary:hover {
  background-color: #e9f7ef; /* 연한 초록색 배경 */
  color: #218838; /* 더 진한 초록색 텍스트 */
  border-color: #218838;
}

</style>