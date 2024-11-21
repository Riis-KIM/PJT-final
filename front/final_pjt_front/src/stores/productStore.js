import { defineStore } from "pinia";

export const useProductStore = defineStore("productStore", {
  state: () => ({
    products: {}, // 상품 데이터를 저장
    cart: [], // 구매 목록을 저장
  }),
  actions: {
    setProduct(product) {
      this.products[product.fin_prdt_cd] = product; // 상품 ID를 키로 저장
    },
    getProduct(id) {
      return this.products[id] || null; // 상품 ID로 데이터 반환
    },
    addToCart(product) {
      const exists = this.cart.find((item) => item.fin_prdt_cd === product.fin_prdt_cd);
      if (!exists) {
        this.cart.push(product); // 구매 목록에 상품 추가
      }
    },
    removeFromCart(productId) {
      this.cart = this.cart.filter((item) => item.fin_prdt_cd !== productId);
    },
    getCart() {
      return this.cart; // 현재 구매 목록 반환
    },
  },
});
