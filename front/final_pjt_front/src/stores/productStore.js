import { defineStore } from "pinia";
import axios from "axios";

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

    async getCart() {
      try {
        const token = localStorage.getItem("token"); // localStorage 또는 다른 저장소에서 토큰 가져오기
        const response = await axios.get(`/accounts/custom/myproducts/`, {
          headers: {
            Authorization: `Token ${token}`, // 헤더에 토큰 추가
          },
        });
        this.cart = response.data || [];

        return response.data;
      } catch (error) {
        console.error("구매 목록을 가져오는 중 오류 발생:", error);
        return [];
      }
    }
  }
});
