<template>
  <div class="container mt-5">
    <!-- 추천 섹션 -->
    <section class="d-flex justify-content-between align-items-center mb-4 section-header">
      <!-- 섹션 제목 -->
      <div>
        <h1 class="fw-bold mb-2 section-title">금리 검색</h1>
        <p class="lead section-subtitle">최적의 금융 상품을 한눈에 비교해보세요</p>
      </div>
    </section>

<!-- 검색 및 필터 -->
<section class="search-section d-flex align-items-end mb-4">
  <!-- 은행 선택 -->
  <div class="search-container flex-grow-1 me-3">
    <label for="bankFilter" class="form-label fw-semibold">은행 선택</label>
    <div class="input-group">
      <input
        id="bankFilter"
        type="text"
        class="form-control form-control-lg"
        placeholder="은행명을 입력하세요"
        v-model="searchQuery"
      />
      <button
        v-if="searchQuery"
        class="btn btn-outline-secondary clear-btn"
        type="button"
        @click="clearSearch"
      >
        ×
      </button>
    </div>
  </div>

  <!-- 상품 유형 선택 버튼 -->
  <div class="btn-group">
    <button
      class="btn btn-product-type"
      :class="{ active: productType === 'deposit' }"
      @click="setProductType('deposit')"
    >
      예금
    </button>
    <button
      class="btn btn-product-type"
      :class="{ active: productType === 'saving' }"
      @click="setProductType('saving')"
    >
      적금
    </button>
  </div>
  </section>

    <!-- 테이블 -->
    <section class="recommendation-section p-4 rounded">
      <h2 class="fw-bold text-center mb-4 list-title">
        {{ productType === 'deposit' ? "예금" : "적금" }} 금리 비교
      </h2>
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-header">
            <tr>
              <th class="sortable" @click="sortTable('kor_co_nm')">금융회사명</th>
              <th class="sortable" @click="sortTable('fin_prdt_nm')">상품명</th>
              <th class="sortable" @click="sortTable('maxRate')">최고금리</th>
              <th>6개월</th>
              <th>12개월</th>
              <th>24개월</th>
              <th>36개월</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredData" :key="item.fin_prdt_cd">
              <td>{{ item.kor_co_nm }}</td>
              <td>
                <button
                  class="btn btn-link p-0 text-decoration-none product-name"
                  @click="goToDetail(item)"
                >
                  {{ item.fin_prdt_nm }}
                </button>
              </td>
              <td>{{ getMaxRate(item.options) }}%</td>
              <td>{{ getTermRate(item.options, 6) }}</td>
              <td>{{ getTermRate(item.options, 12) }}</td>
              <td>{{ getTermRate(item.options, 24) }}</td>
              <td>{{ getTermRate(item.options, 36) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useProductStore } from "@/stores/productStore";
import axios from "axios";

const searchQuery = ref("");
const sortKey = ref("");
const sortOrder = ref(1);
const tableData = ref([]);
const productType = ref("deposit");
const router = useRouter();
const productStore = useProductStore();

// 검색어 초기화 함수
const clearSearch = () => {
  searchQuery.value = "";
};

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

// 필터링된 데이터
const filteredData = computed(() => {
  let filtered = tableData.value[productType.value] || [];

  if (searchQuery.value) {
    filtered = filtered.filter((item) =>
      item.kor_co_nm.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  if (sortKey.value) {
    filtered = filtered.sort((a, b) => {
      let aValue = a[sortKey.value];
      let bValue = b[sortKey.value];

      if (sortKey.value === "maxRate") {
        aValue = parseFloat(getMaxRate(a.options));
        bValue = parseFloat(getMaxRate(b.options));
      }

      return aValue < bValue ? -1 * sortOrder.value : aValue > bValue ? 1 * sortOrder.value : 0;
    });
  }

  return filtered;
});

// 정렬 함수
const sortTable = (key) => {
  if (key === sortKey.value) {
    // 같은 키를 다시 클릭하면 정렬 방향을 변경
    sortOrder.value *= -1;
  } else {
    // 새로운 키로 정렬할 때는 오름차순으로 시작
    sortKey.value = key;
    sortOrder.value = 1;
  }
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

.search-container {
  position: relative;
}

.clear-btn {
  position: absolute;
  top: 50%;
  right: 40px;
  transform: translateY(-2%);
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #868e96;
  cursor: pointer;
}

.clear-btn:hover {
  color: #343a40;
}

.recommendation-section {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  padding: 20px;
}

.table {
  text-align: center;
  font-family: 'Open Sans', sans-serif;
}

.table-header {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
  background-color: #e9ecef;
  color: #495057;
}

.table-row:hover {
  background-color: #f1f3f5;
}

.product-name {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
  color: #495057;
  transition: color 0.3s;
}

.product-name:hover {
  text-decoration: underline;
  color: #212529;
}

.list-title {
  font-family: 'Roboto', sans-serif;
  font-weight: 700;
}
</style>