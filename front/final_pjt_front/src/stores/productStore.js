// src/stores/productStore.js
import { defineStore } from 'pinia';

export const useProductStore = defineStore('productStore', {
  state: () => ({
    selectedProduct: null, // 선택된 상품 데이터 저장
  }),
  actions: {
    setProduct(product) {
      this.selectedProduct = product;
    },
  },
})