<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">🛒 구매 목록</h1>
    <div v-if="cart.length">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>금융회사명</th>
            <th>상품명</th>
            <th>최고금리</th>
            <th>삭제</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cart" :key="item.fin_prdt_cd">
            <td>{{ item.kor_co_nm }}</td>
            <td>{{ item.fin_prdt_nm }}</td>
            <td>{{ item.options ? getMaxRate(item.options) + "%" : "-" }}</td>
            <td>
              <button
                class="btn btn-danger btn-sm"
                @click="removeFromCart(item.fin_prdt_cd)"
              >
                삭제
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p class="text-center">구매 목록이 비어 있습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useProductStore } from "@/stores/productStore";

const productStore = useProductStore();

// 구매 목록 가져오기
const cart = computed(() => productStore.getCart());

// 최고 금리를 반환하는 함수
const getMaxRate = (options) => {
  const rates = options?.map((opt) => opt.intr_rate).filter((rate) => rate !== null) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : "-";
};

// 구매 목록에서 상품 삭제
const removeFromCart = (productId) => {
  productStore.removeFromCart(productId);
};
</script>

<style scoped>
.container {
  margin-top: 2rem;
}

.table {
  text-align: center;
}

th, td {
  vertical-align: middle;
}

button {
  font-size: 0.9rem;
}
</style>
