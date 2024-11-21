import { defineStore } from "pinia";

export const useProductStore = defineStore("productStore", {
  state: () => ({
    products: {}, // 상품 데이터를 저장할 객체
  }),
  actions: {
    setProduct(product) {
      this.products[product.fin_prdt_cd] = product; // 상품 ID를 키로 저장
    },
    getProduct(id) {
      return this.products[id] || null; // 상품 ID로 데이터 반환
    },
  },
});
