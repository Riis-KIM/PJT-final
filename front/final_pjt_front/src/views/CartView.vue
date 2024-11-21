<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">🛒 구매 목록</h1>
    <div v-if="cart?.joined_deposits?.length">
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
          <tr v-for="item in cart.joined_deposits" :key="item.fin_prdt_cd">
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
import { ref, onMounted } from "vue";
import axios from "axios";
import { useProductStore } from "@/stores/productStore";

const productStore = useProductStore();
const cart = ref(null);

// API를 호출하여 구매 목록 가져오기
const fetchCart = async () => {
  try {
    const token = localStorage.getItem("token"); // 토큰 가져오기
    const response = await axios.get("/accounts/custom/myproducts/", {
      headers: {
        Authorization: `Token ${token}`, // 헤더에 토큰 추가
      },
    });
    cart.value = response.data; // 서버로부터 가져온 데이터를 cart에 저장
    productStore.setCart(cart.value); // Pinia 스토어에 저장
  } catch (error) {
    console.error("구매 목록을 가져오는 중 오류 발생:", error);
  }
};

// 최고 금리를 반환하는 함수
const getMaxRate = (options) => {
  const rates = options?.map((opt) => opt.intr_rate).filter((rate) => rate !== null) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : "-";
};

// 구매 목록에서 상품 삭제
const removeFromCart = async (productId) => {
  try {
    const token = localStorage.getItem("token");
    await axios.post(`/api/accounts/custom/remove/${productId}/`, null, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    cart.value.joined_deposits = cart.value.joined_deposits.filter(
      (item) => item.fin_prdt_cd !== productId
    );
  } catch (error) {
    console.error("항목을 제거하는 중 오류 발생:", error);
  }
};

onMounted(() => {
  fetchCart(); // 컴포넌트가 마운트될 때 구매 목록 가져오기
});
</script>

<style scoped>
.container {
  margin-top: 2rem;
}

.table {
  text-align: center;
}

th,
td {
  vertical-align: middle;
}

button {
  font-size: 0.9rem;
}
</style>
