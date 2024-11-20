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

  // 게시글 상세 조회
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

  // stores/articles.js
const createArticle = function(articleData) {
  return new Promise((resolve, reject) => {
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
        resolve(res.data)
      })
      .catch((err) => {
        console.error(err)
        alert('게시글 작성에 실패했습니다.')
        reject(err)
      })
  })
}

const updateArticle = function(articleId, articleData) {
  return new Promise((resolve, reject) => {
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
        resolve(res.data)
      })
      .catch((err) => {
        console.error(err)
        alert('게시글 수정에 실패했습니다.')
        reject(err)
      })
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
        articles.value = articles.value.filter(article => article.id !== articleId)
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

  return {
    articles,
    article,
    getArticles,
    getArticle,
    createArticle,
    updateArticle,
    deleteArticle,
    createComment,
    deleteComment
  }
})