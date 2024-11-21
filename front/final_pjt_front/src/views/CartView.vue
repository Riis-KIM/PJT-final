<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">🛒 구매 목록</h1>

    <!-- 예금 목록 -->
    <div v-if="cart?.joined_deposits?.length" class="mb-5">
      <h2 class="fw-bold text-center">예금 목록</h2>
      <table class="table table-striped table-hover mt-3">
        <thead class="table-dark">
          <tr>
            <th class="text-center" style="width: 25%;">금융회사명</th>
            <th class="text-center" style="width: 40%;">상품명</th>
            <th class="text-center" style="width: 20%;">최고금리</th>
            <th class="text-center" style="width: 15%;">삭제</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cart.joined_deposits" :key="item.fin_prdt_cd">
            <td class="text-center">{{ item.kor_co_nm }}</td>
            <td class="text-center">
              <button 
                class="btn btn-link p-0 text-decoration-none"
                @click="goToDetail(item, 'deposit')"
              >
                {{ item.fin_prdt_nm }}
              </button>
            </td>
            <td class="text-center">{{ item.options ? getMaxRate(item.options) + "%" : "-" }}</td>
            <td class="text-center">
              <button
                class="btn btn-danger btn-sm"
                @click="removeDeposit(item.fin_prdt_cd)"
              >
                삭제
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 적금 목록 -->
    <div v-if="cart?.joined_savings?.length">
      <h2 class="fw-bold text-center">적금 목록</h2>
      <table class="table table-striped table-hover mt-3">
        <thead class="table-dark">
          <tr>
            <th class="text-center" style="width: 25%;">금융회사명</th>
            <th class="text-center" style="width: 40%;">상품명</th>
            <th class="text-center" style="width: 20%;">최고금리</th>
            <th class="text-center" style="width: 15%;">삭제</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cart.joined_savings" :key="item.fin_prdt_cd">
            <td class="text-center">{{ item.kor_co_nm }}</td>
            <td class="text-center">
              <button 
                class="btn btn-link p-0 text-decoration-none"
                @click="goToDetail(item, 'saving')"
              >
                {{ item.fin_prdt_nm }}
              </button>
            </td>
            <td class="text-center">{{ item.options ? getMaxRate(item.options) + "%" : "-" }}</td>
            <td class="text-center">
              <button
                class="btn btn-danger btn-sm"
                @click="removeSaving(item.fin_prdt_cd)"
              >
                삭제
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 목록이 비었을 때 -->
    <div v-else>
      <p class="text-center text-muted">구매 목록이 비어 있습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useProductStore } from "@/stores/productStore";
import { useRouter } from "vue-router";

const productStore = useProductStore();
const cart = ref(null);
const router = useRouter();

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
  } catch (error) {
    console.error("구매 목록을 가져오는 중 오류 발생:", error);
  }
};

// 최고 금리를 반환하는 함수
const getMaxRate = (options) => {
  const rates = options?.map((opt) => opt.intr_rate).filter((rate) => rate !== null) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : "-";
};

// 예금 목록에서 상품 삭제
const removeDeposit = async (productId) => {
  try {
    const token = localStorage.getItem("token");
    await axios.post(`/api/v1/deposits/${productId}/join/`, null, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    cart.value.joined_deposits = cart.value.joined_deposits.filter(
      (item) => item.fin_prdt_cd !== productId
    );
    alert("예금 상품이 삭제되었습니다."); // 성공 메시지
  } catch (error) {
    console.error("예금 항목을 제거하는 중 오류 발생:", error);
  }
};

// 적금 목록에서 상품 삭제
const removeSaving = async (productId) => {
  try {
    const token = localStorage.getItem("token");
    await axios.post(`/api/v1/savings/${productId}/join/`, null, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    cart.value.joined_savings = cart.value.joined_savings.filter(
      (item) => item.fin_prdt_cd !== productId
    );
    alert("적금 상품이 삭제되었습니다."); // 성공 메시지
  } catch (error) {
    console.error("적금 항목을 제거하는 중 오류 발생:", error);
  }
};

// 상품 상세 페이지로 이동
const goToDetail = (item, producttype) => {
  productStore.setProduct(item);
  router.push({ name: "DetailProduct", params: { id: item.fin_prdt_cd, type: producttype } });
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
  text-decoration: none;
}
</style>
