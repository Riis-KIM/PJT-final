<template>
  <div class="container mt-5">
    <div class="card">
      <!-- 게시글 내용 -->
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h2 class="card-title">{{ articleStore.article?.title }}</h2>
          <small class="text-muted">작성자: {{ articleStore.article?.username }}</small>
        </div>
        <p class="card-text">{{ articleStore.article?.content }}</p>
        <div class="text-muted small mb-3">
          작성일: {{ formatDate(articleStore.article?.created_at) }}
        </div>
        
        <!-- 수정/삭제 버튼 (작성자인 경우만 표시) -->
        <div v-if="isAuthor" class="mb-4">
          <button class="btn btn-warning me-2" @click="goToEdit">수정</button>
          <button class="btn btn-danger" @click="deleteArticle">삭제</button>
        </div>
      </div>

      <!-- 댓글 섹션 -->
      <div class="card-footer">
        <h4>댓글 {{ articleStore.article?.comments?.length || 0 }}개</h4>
        
        <!-- 댓글 작성 폼 -->
        <div class="mb-3">
          <textarea 
            v-model="commentContent" 
            class="form-control"
            rows="3"
            placeholder="댓글을 입력하세요"
          ></textarea>
          <button 
            class="btn btn-primary mt-2"
            @click="submitComment"
          >
            댓글 작성
          </button>
        </div>

        <!-- 댓글 목록 -->
        <div v-if="articleStore.article?.comments?.length" class="mt-4">
          <div v-for="comment in articleStore.article.comments" 
               :key="comment.id" 
               class="border-bottom py-3">
            <div class="d-flex justify-content-between">
              <div class="w-100">
                <strong>{{ comment.username }}</strong>
                <!-- 수정 모드일 때는 입력창, 아닐 때는 텍스트 표시 -->
                <div v-if="editingCommentId === comment.id">
                  <textarea 
                    v-model="editingContent" 
                    class="form-control my-2"
                    rows="2"
                  ></textarea>
                  <div class="d-flex gap-2">
                    <button 
                      class="btn btn-sm btn-success"
                      @click="updateComment(comment.id)"
                    >
                      확인
                    </button>
                    <button 
                      class="btn btn-sm btn-secondary"
                      @click="cancelEdit"
                    >
                      취소
                    </button>
                  </div>
                </div>
                <div v-else>
                  <p class="mb-1">{{ comment.content }}</p>
                  <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
                </div>
              </div>
              <!-- 댓글 수정/삭제 버튼 (작성자인 경우만 표시) -->
              <div v-if="comment.username === authStore.user?.username">
                <button 
                  class="btn btn-sm btn-warning me-2"
                  @click="startEdit(comment)"
                >
                  수정
                </button>
                <button 
                  class="btn btn-sm btn-danger"
                  @click="deleteComment(comment.id)"
                >
                  삭제
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const articleStore = useArticleStore()
const authStore = useAuthStore()

const commentContent = ref('')
const editingCommentId = ref(null)
const editingContent = ref('')

// 현재 사용자가 글 작성자인지 확인
const isAuthor = computed(() => {
  return articleStore.article?.username === authStore.user?.username
})

// 날짜 포맷팅
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR')
}

// 게시글 삭제
const deleteArticle = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    articleStore.deleteArticle(route.params.id)
    router.push({ name: 'community' })
  }
}

// 게시글 수정 페이지로 이동
const goToEdit = () => {
  router.push({ 
    name: 'articleEdit', 
    params: { id: route.params.id }
  })
}

// 댓글 작성
const submitComment = async () => {
  if (!commentContent.value.trim()) return
  
  await articleStore.createComment(route.params.id, {
    content: commentContent.value
  })
  commentContent.value = ''
}

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    await articleStore.deleteComment(route.params.id, commentId)
  }
}

// 댓글 수정 시작
const startEdit = (comment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

// 댓글 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

// 댓글 수정 제출
const updateComment = async (commentId) => {
  if (!editingContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }

  await articleStore.updateComment(route.params.id, commentId, {
    content: editingContent.value
  })
  cancelEdit()
}

// 컴포넌트 마운트 시 게시글 정보 가져오기
onMounted(() => {
  articleStore.getArticle(route.params.id)
})
</script>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.w-100 {
  width: 100%;
}
</style>