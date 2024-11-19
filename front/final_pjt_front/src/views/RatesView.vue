<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">🔍 금리 검색</h1>

    <!-- 검색 기능 -->
    <div class="mb-3">
      <label for="bankFilter" class="form-label">은행 선택</label>
      <input
        id="bankFilter"
        type="text"
        class="form-control"
        placeholder="은행명을 입력하세요"
        v-model="searchQuery"
      />
    </div>

    <!-- 테이블 -->
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th @click="sortTable('kor_co_nm')" style="cursor: pointer;">
            금융회사명
          </th>
          <th @click="sortTable('fin_prdt_nm')" style="cursor: pointer;">
            상품명
          </th>
          <th @click="sortTable('intr_rate')" style="cursor: pointer;">
            저축금리
          </th>
          <th @click="sortTable('six_months')" style="cursor: pointer;">
            6개월
          </th>
          <th @click="sortTable('twelve_months')" style="cursor: pointer;">
            12개월
          </th>
          <th @click="sortTable('twenty_four_months')" style="cursor: pointer;">
            24개월
          </th>
          <th @click="sortTable('thirty_six_months')" style="cursor: pointer;">
            36개월
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in filteredData" :key="index">
          <td>{{ item.kor_co_nm }}</td>
          <td>{{ item.fin_prdt_nm }}</td>
          <td>{{ item.intr_rate }}%</td>
          <td>{{ item.six_months || 'N/A' }}</td>
          <td>{{ item.twelve_months || 'N/A' }}</td>
          <td>{{ item.twenty_four_months || 'N/A' }}</td>
          <td>{{ item.thirty_six_months || 'N/A' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";

export default {
  name: "RatesTable",
  setup() {
    const searchQuery = ref(""); // 검색어
    const sortKey = ref(""); // 정렬 기준
    const sortOrder = ref(1); // 정렬 순서 (1: 오름차순, -1: 내림차순)
    const tableData = ref([]); // API 데이터

    // API 호출
    const fetchData = async () => {
      try {
        // Django API 호출
        const depositResponse = await axios.get("http://127.0.0.1:8000/api/v1/deposits/");
        const savingResponse = await axios.get("http://127.0.0.1:8000/api/v1/savings/");

        // 예금 및 적금 데이터를 결합
        const depositData = depositResponse.data.map((item) => ({
          kor_co_nm: item.kor_co_nm, // 금융회사명
          fin_prdt_nm: item.fin_prdt_nm, // 상품명
          intr_rate: item.intr_rate || "N/A", // 기본 금리
          six_months: item.six_months_rate || null,
          twelve_months: item.twelve_months_rate || null,
          twenty_four_months: item.twenty_four_months_rate || null,
          thirty_six_months: item.thirty_six_months_rate || null,
        }));

        const savingData = savingResponse.data.map((item) => ({
          kor_co_nm: item.kor_co_nm, // 금융회사명
          fin_prdt_nm: item.fin_prdt_nm, // 상품명
          intr_rate: item.intr_rate || "N/A", // 기본 금리
          six_months: item.six_months_rate || null,
          twelve_months: item.twelve_months_rate || null,
          twenty_four_months: item.twenty_four_months_rate || null,
          thirty_six_months: item.thirty_six_months_rate || null,
        }));

        // 데이터 결합
        tableData.value = [...depositData, ...savingData];
      } catch (error) {
        console.error("데이터를 가져오는 중 오류 발생:", error);
      }
    };

    // 필터링된 데이터
    const filteredData = computed(() => {
      let filtered = tableData.value;

      // 검색어 필터
      if (searchQuery.value) {
        filtered = filtered.filter((item) =>
          item.kor_co_nm.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
      }

      // 정렬
      if (sortKey.value) {
        filtered = filtered.sort((a, b) => {
          if (a[sortKey.value] < b[sortKey.value]) return -1 * sortOrder.value;
          if (a[sortKey.value] > b[sortKey.value]) return 1 * sortOrder.value;
          return 0;
        });
      }

      return filtered;
    });

    // 정렬 함수
    const sortTable = (key) => {
      if (sortKey.value === key) {
        sortOrder.value *= -1; // 동일한 열 클릭 시 정렬 순서 변경
      } else {
        sortKey.value = key;
        sortOrder.value = 1; // 기본 오름차순
      }
    };

    // API 데이터 가져오기
    onMounted(() => {
      fetchData();
    });

    return {
      searchQuery,
      filteredData,
      sortTable,
    };
  },
};
</script>

<style scoped>
table {
  width: 100%;
  text-align: center;
}

th {
  background-color: #f8f9fa;
  user-select: none;
}

th:hover {
  background-color: #e9ecef;
}
</style>
