<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4 text-center">상품 상세정보</h1>
    <div v-if="product" class="card shadow-lg p-4">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">{{ product.fin_prdt_nm }}</h2>
        <p class="card-text">
          <strong>금융회사명:</strong> {{ product.kor_co_nm }}
        </p>
        <p class="card-text">
          <strong>가입제한:</strong> {{ product.join_deny === 1 ? "개인" : "법인" }}
        </p>
        <p class="card-text"><strong>우대조건:</strong></p>
        <ul class="list-group mb-3">
          <li
            class="list-group-item"
            v-for="condition in formatConditions(product.spcl_cnd)"
            :key="condition"
          >
            {{ condition }}
          </li>
        </ul>
        <p class="card-text">
          <strong>가입방법:</strong> {{ product.join_way }}
        </p>
      </div>
    </div>
    <div v-else class="text-center mt-5">
      <p class="text-muted">상품 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useProductStore } from "@/stores/productStore"; // Pinia 스토어 사용

const route = useRoute();
const productStore = useProductStore();
const product = ref(null); // 선택된 상품 데이터를 저장

// 우대 조건 포맷팅 함수
const formatConditions = (conditions) => {
  if (!conditions) return ["없음"];
  return conditions.split("\n").filter((line) => line.trim() !== "");
};

// 새로고침 시 데이터를 복원하기 위한 함수
const loadProductFromLocalStorage = () => {
  const storedProduct = localStorage.getItem("selectedProduct");
  if (storedProduct) {
    return JSON.parse(storedProduct);
  }
  return null;
};

onMounted(() => {
  const storedProduct = loadProductFromLocalStorage();

  // Pinia 스토어에서 데이터를 가져오거나 localStorage에서 복원
  product.value = productStore.getProduct(route.params.id) || storedProduct;

  // localStorage에 데이터 저장
  if (product.value) {
    localStorage.setItem("selectedProduct", JSON.stringify(product.value));
  }
});
</script>

<style scoped>
.container {
  margin-top: 2rem;
}

/* 카드 스타일 */
.card {
  border-radius: 10px;
}

.card-title {
  font-size: 1.75rem;
  font-weight: bold;
}

.card-text {
  font-size: 1.1rem;
}

.list-group-item {
  font-size: 1rem;
}
</style>
