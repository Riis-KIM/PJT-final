<template>
  <div class="container mt-5">
    <!-- 추천 섹션 -->
    <section class="d-flex justify-content-between align-items-center mb-4 section-header">
      <!-- 섹션 제목 -->
      <div>
        <h1 class="fw-bold mb-2 section-title">금융상품 추천</h1>
        <p class="lead section-subtitle">당신에게 꼭 맞는 금융상품을 찾아보세요</p>
      </div>

      <!-- 상품 유형 선택 버튼 -->
      <div class="btn-group">
        <button
          class="btn btn-lg btn-product-type"
          :class="{ active: productType === 'deposit' }"
          @click="setProductType('deposit')"
        >
          예금
        </button>
        <button
          class="btn btn-lg btn-product-type"
          :class="{ active: productType === 'saving' }"
          @click="setProductType('saving')"
        >
          적금
        </button>
      </div>
    </section>

    <!-- 추천 상품 리스트 -->
    <section class="recommendation-section-wrapper">
      <div class="recommendation-section p-4 rounded shadow-sm">
        <h2 class="fw-bold text-center mb-4 list-title">{{ productType === 'deposit' ? "예금" : "적금" }} 추천</h2>
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-header">
              <tr>
                <th class="rank-column">순위</th>
                <th>금융회사명</th>
                <th>상품명</th>
                <th>인기도</th>
                <th>최고금리</th>
                <th>12개월 금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in topProducts" :key="item.fin_prdt_cd" class="table-row">
                <td>{{ index + 1 }}</td>
                <td>{{ item.kor_co_nm }}</td>
                <td>
                  <button
                    class="btn btn-link p-0 text-decoration-none product-name"
                    @click="goToDetail(item)"
                  >
                    {{ item.fin_prdt_nm }}
                  </button>
                </td>
                <td>{{ item.popularity?.popularity || 0 }}</td>
                <td>{{ getMaxRate(item.options) }}%</td>
                <td>{{ getTermRate(item.options, 12) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useProductStore } from "@/stores/productStore";
import axios from "axios";

const productType = ref("deposit");
const tableData = ref([]);
const router = useRouter();
const productStore = useProductStore();

// 상품 유형 설정
const setProductType = (type) => {
  productType.value = type;
};

// 특정 기간의 금리를 반환하는 함수
const getTermRate = (options, term) => {
  const option = options?.find((opt) => opt.save_trm === term);
  return option && option.intr_rate !== null ? `${option.intr_rate}%` : "-";
};

// 최고 금리를 반환하는 함수
const getMaxRate = (options) => {
  const rates = options?.map((opt) => opt.intr_rate).filter((rate) => rate !== null) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : "-";
};

// 상위 10개 상품 계산
const topProducts = computed(() => {
  const products = tableData.value[productType.value] || [];
  return [...products]
    .sort((a, b) => (b.popularity?.popularity || 0) - (a.popularity?.popularity || 0))
    .slice(0, 10);
});

// API 호출
const fetchData = async () => {
  try {
    const [depositResponse, savingResponse] = await Promise.all([
      axios.get("http://127.0.0.1:8000/api/v1/deposits/"),
      axios.get("http://127.0.0.1:8000/api/v1/savings/"),
    ]);

    tableData.value = {
      deposit: depositResponse.data,
      saving: savingResponse.data,
    };
  } catch (error) {
    console.error("데이터를 가져오는 중 오류 발생:", error);
  }
};

// 상품 상세 페이지로 이동
const goToDetail = (item) => {
  productStore.setProduct(item);
  router.push({ name: "DetailProduct", params: { id: item.fin_prdt_cd, type: productType.value } });
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600;700&display=swap');

body {
  font-family: 'Roboto', 'Open Sans', sans-serif;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-title {
  font-family: 'Roboto', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #343a40;
}

.section-subtitle {
  font-family: 'Open Sans', sans-serif;
  font-weight: 400;
  color: #6c757d;
}

.recommendation-section-wrapper {
  margin-top: 2rem;
}

.recommendation-section {
  background: #f9f9f9;
  border: 1px solid #d9d9d9;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.product-name {
  color: #666666;
  font-weight: bold;
}

.product-name:hover {
  color: #444444;
}

.table-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

/* 버튼 스타일 */
.btn-product-type {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
  background-color: #e9ecef;
  color: #343a40;
  border: 1px solid #ced4da;
  border-radius: 30px;
  padding: 10px 20px;
  height: 48px;
  transition: all 0.3s ease-in-out;
}

.btn-product-type.active {
  background-color: #495057;
  color: white;
}

.btn-product-type:hover {
  background-color: #868e96;
  color: white;
}
</style>
