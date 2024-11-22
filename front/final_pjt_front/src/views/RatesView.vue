<template>
  <div class="container mt-5">
    <div class="text-center">
      <h1 class="fw-bold mb-4">🔍 금리 검색</h1>
    </div>

    <!-- 검색 및 필터 -->
    <div class="row mb-4">
      <div class="col-lg-6 col-md-8 mx-auto position-relative search-container">
        <label for="bankFilter" class="form-label fw-semibold">은행 선택</label>
        <input
          id="bankFilter"
          type="text"
          class="form-control form-control-lg"
          placeholder="은행명을 입력하세요"
          v-model="searchQuery"
        />
        <button
          v-if="searchQuery"
          class="btn clear-btn"
          @click="clearSearch"
        >
          ×
        </button>
      </div>
      <div class="col-lg-6 col-md-8 mx-auto text-center mt-3">
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

    <!-- 테이블 -->
    <div class="table-responsive shadow-sm rounded">
      <table class="table table-striped table-hover align-middle">
        <thead class="table-dark">
          <tr>
            <th @click="sortTable('kor_co_nm')" class="sortable">금융회사명</th>
            <th @click="sortTable('fin_prdt_nm')" class="sortable">상품명</th>
            <th @click="sortTable('maxRate')" class="sortable">최고금리</th>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useProductStore } from "@/stores/productStore";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const searchQuery = ref("");
const sortKey = ref("");
const sortOrder = ref(1);
const tableData = ref([]);
const productType = ref("deposit");
const router = useRouter();
const productStore = useProductStore();
const authStore = useAuthStore();

// 검색어 초기화 함수
const clearSearch = () => {
  searchQuery.value = "";
};

// 상품 유형 설정 버튼 이벤트
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
const fetchData = () => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/api/v1/deposits/'
  })
    .then((depositResponse) => {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/savings/'
      })
        .then((savingResponse) => {
          tableData.value = {
            deposit: depositResponse.data,
            saving: savingResponse.data
          }
        })
    })
    .catch((err) => {
      console.error("데이터를 가져오는 중 오류 발생:", err)
    })
}

// 상품 상세 페이지로 이동
const goToDetail = (item) => {
  // 상품 클릭 시 인기도 업데이트 요청
  axios({
    method: 'put',
    url: `/api/v1/${productType.value}s/${item.fin_prdt_cd}/popularity/`,
    data: { click: true },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .catch((err) => {
      console.error('인기도 업데이트 실패:', err)
    })
  
  // 페이지 이동
  productStore.setProduct(item)
  router.push({ 
    name: "DetailProduct", 
    params: { 
      id: item.fin_prdt_cd, 
      type: productType.value 
    }
  })
}

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
  sortKey.value = key === sortKey.value ? "" : key;
  sortOrder.value = sortKey.value === key && sortOrder.value === 1 ? -1 : 1;
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
table {
  text-align: center;
}

th {
  background-color: #f8f9fa;
  user-select: none;
}

th:hover {
  background-color: #e9ecef;
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

/* 검색창 초기화 버튼 스타일 */
/* 검색창 초기화 버튼 스타일 */
.clear-btn {
  position: absolute;
  top: 0;
  right: 20px;
  height: 130%; /* 부모 요소 높이에 맞추기 */
  display: flex;
  align-items: center; /* 수직 중앙 정렬 */
  justify-content: center; /* 수평 중앙 정렬 */
  border: none;
  background: transparent;
  font-size: 1.5rem;
  color: #495057;
  cursor: pointer;
  padding: 0;
}

.clear-btn:hover {
  color: #0d6efd;
}
</style>
