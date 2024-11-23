// stores/articles.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export const useArticleStore = defineStore('articles', () => {
  const authStore = useAuthStore()
  const articles = ref([])
  const article = ref(null)

  // 게시글 목록 조회
  const getArticles = function() {
    axios({
      method: 'get',
      url: '/articles/',
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => {
        console.error(err)
        alert('게시글을 불러오는데 실패했습니다.')
      })
  }

// stores/articles.js
const getArticle = function(articleId) {
  axios({
    method: 'get',
    url: `/articles/${articleId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      article.value = res.data
    })
    .catch((err) => {
      console.error(err)
      alert('게시글을 불러오는데 실패했습니다.')
    })
}
  // 게시글 생성
  const createArticle = function(articleData) {
    axios({
      method: 'post',
      url: '/articles/',
      data: articleData,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then((res) => {
        articles.value.push(res.data)
        alert('게시글이 작성되었습니다.')
      })
      .catch((err) => {
        console.error(err)
        alert('게시글 작성에 실패했습니다.')
      })
  }
  
    // 게시글 수정
  const updateArticle = function(articleId, articleData) {
    axios({
      method: 'put',
      url: `/articles/${articleId}/`,
      data: articleData,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then((res) => {
        article.value = res.data
        alert('게시글이 수정되었습니다.')
      })
      .catch((err) => {
        console.error(err)
        alert('게시글 수정에 실패했습니다.')
      })
  }

  // 게시글 삭제
  const deleteArticle = function(articleId) {
    axios({
      method: 'delete',
      url: `/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(() => {
        getArticles()
        alert('게시글이 삭제되었습니다.')
      })
      .catch((err) => {
        console.error(err)
        alert('게시글 삭제에 실패했습니다.')
      })
  }

  // 댓글 작성
  const createComment = function(articleId, commentData) {
    axios({
      method: 'post',
      url: `/articles/${articleId}/comments/`,
      data: commentData,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then((res) => {
        article.value.comments.push(res.data)
        alert('댓글이 작성되었습니다.')
      })
      .catch((err) => {
        console.error(err)
        alert('댓글 작성에 실패했습니다.')
      })
  }

  // 댓글 삭제
  const deleteComment = function(articleId, commentId) {
    axios({
      method: 'delete',
      url: `/articles/${articleId}/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(() => {
        article.value.comments = article.value.comments.filter(comment => comment.id !== commentId)
        alert('댓글이 삭제되었습니다.')
      })
      .catch((err) => {
        console.error(err)
        alert('댓글 삭제에 실패했습니다.')
      })
  }

// 댓글 수정
const updateComment = function(articleId, commentId, commentData) {
  axios({
    method: 'put',
    url: `/articles/${articleId}/comments/${commentId}/update/`,
    data: {
      content: commentData.content
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      // 현재 게시글의 댓글 목록에서 수정된 댓글 찾아서 업데이트
      const commentIndex = article.value.comments.findIndex(c => c.id === commentId)
      if (commentIndex !== -1) {
        article.value.comments[commentIndex] = res.data
      }
      alert('댓글이 수정되었습니다.')
    })
    .catch((err) => {
      console.error(err)
      alert('댓글 수정에 실패했습니다.')
    })
}

  return {
    articles,
    article,
    getArticles,
    getArticle,
    createArticle,
    updateArticle,
    deleteArticle,
    createComment,
    deleteComment,
    updateComment,
  }
})