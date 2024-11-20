<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">상품 상세정보</h1>
    <div v-if="product">
      <p><strong>금융회사명:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>상품명:</strong> {{ product.fin_prdt_nm }}</p>
      <p><strong>가입제한:</strong> {{ product.join_deny === 1 ? "개인" : "법인" }}</p>
      <p><strong>우대조건:</strong></p>
      <ul>
        <li v-for="condition in formatConditions(product.spcl_cnd)" :key="condition">
          {{ condition }}
        </li>
      </ul>
      <p><strong>가입방법:</strong> {{ product.join_way }}</p>
    </div>
    <div v-else>
      <p>상품 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useProductStore } from "@/stores/productStore"; // Pinia 스토어 임포트

const route = useRoute();
const product = computed(() => JSON.parse(route.query.product || "{}"));

// 우대 조건 포맷팅 함수
const formatConditions = (conditions) => {
  if (!conditions) return ["없음"];
  return conditions.split("\n").filter((line) => line.trim() !== "");
};
</script>

<style scoped>
.container {
  margin-top: 2rem;
}
</style>
