// stores/productStore.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('productStore', () => {
  // state
  const products = ref({})
  const cart = ref([])

  // actions
  const setProduct = (product) => {
    products.value[product.fin_prdt_cd] = product
  }

  const getProduct = (id) => {
    return products.value[id] || null
  }

  const addToCart = (product) => {
    const exists = cart.value.find((item) => item.fin_prdt_cd === product.fin_prdt_cd)
    if (!exists) {
      cart.value.push(product)
    }
  }

  const removeFromCart = (productId) => {
    cart.value = cart.value.filter((item) => item.fin_prdt_cd !== productId)
  }

  const getCart = () => {
    const token = localStorage.getItem('token')
    
    axios({
      method: 'get',
      url: '/accounts/custom/myproducts/',
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        cart.value = res.data || []
        return res.data
      })
      .catch((err) => {
        console.error('구매 목록을 가져오는 중 오류 발생:', err)
        return []
      })
  }

  return {
    products,
    cart,
    setProduct,
    getProduct,
    addToCart,
    removeFromCart,
    getCart
  }
})