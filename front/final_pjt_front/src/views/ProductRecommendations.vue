<template>
  <div class="container mt-5">
    <div class="text-center">
      <h1 class="fw-bold mb-4">🏆 인기 금융상품</h1>
    </div>

    <!-- 상품 유형 선택 -->
    <div class="row mb-4">
      <div class="col-lg-6 col-md-8 mx-auto text-center">
        <div class="btn-group">
          <button
            class="btn btn-lg"
            :class="productType === 'deposit' ? 'btn-primary' : 'btn-outline-primary'"
            @click="setProductType('deposit')"
          >
            예금
          </button>
          <button
            class="btn btn-lg"
            :class="productType === 'saving' ? 'btn-primary' : 'btn-outline-primary'"
            @click="setProductType('saving')"
          >
            적금
          </button>
        </div>
      </div>
    </div>

    <!-- 인기 상품 테이블 -->
    <div class="table-responsive shadow-sm rounded">
      <table class="table table-striped table-hover align-middle">
        <thead class="table-dark">
          <tr>
            <th>순위</th>
            <th>금융회사명</th>
            <th>상품명</th>
            <th>인기도</th>
            <th>최고금리</th>
            <th>12개월 금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in topProducts" :key="item.fin_prdt_cd">
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
table {
  text-align: center;
}

.product-name {
  font-weight: bold;
  color: #495057;
  transition: color 0.3s;
}

.product-name:hover {
  color: #0d6efd;
  text-decoration: underline;
}

.btn-group {
  margin-bottom: 1rem;
}

.table-responsive {
  max-width: 100%;
  overflow-x: auto;
}
</style>