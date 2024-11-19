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
          <th @click="sortTable('submissionDate')" style="cursor: pointer;">
            공시 제출일수
          </th>
          <th @click="sortTable('bank')" style="cursor: pointer;">
            금융회사명
          </th>
          <th @click="sortTable('productName')" style="cursor: pointer;">
            상품명
          </th>
          <th @click="sortTable('sixMonthsRate')" style="cursor: pointer;">
            6개월
          </th>
          <th @click="sortTable('twelveMonthsRate')" style="cursor: pointer;">
            12개월
          </th>
          <th @click="sortTable('twentyFourMonthsRate')" style="cursor: pointer;">
            24개월
          </th>
          <th @click="sortTable('thirtySixMonthsRate')" style="cursor: pointer;">
            36개월
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in filteredData" :key="index">
          <td>{{ item.submissionDate }}</td>
          <td>{{ item.bank }}</td>
          <td>{{ item.productName }}</td>
          <td>{{ item.sixMonthsRate }}</td>
          <td>{{ item.twelveMonthsRate }}</td>
          <td>{{ item.twentyFourMonthsRate }}</td>
          <td>{{ item.thirtySixMonthsRate }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, computed } from "vue";

export default {
  name: "RatesTable",
  setup() {
    const searchQuery = ref(""); // 검색어
    const sortKey = ref(""); // 정렬 기준
    const sortOrder = ref(1); // 정렬 순서 (1: 오름차순, -1: 내림차순)

    // 예시 데이터
    const tableData = ref([
      {
        submissionDate: "202302",
        bank: "신한은행",
        productName: "상품A",
        sixMonthsRate: 3.5,
        twelveMonthsRate: 3.8,
        twentyFourMonthsRate: 4.0,
        thirtySixMonthsRate: 4.2,
      },
      {
        submissionDate: "202302",
        bank: "우리은행",
        productName: "상품B",
        sixMonthsRate: 3.0,
        twelveMonthsRate: 3.5,
        twentyFourMonthsRate: 3.7,
        thirtySixMonthsRate: 3.9,
      },
      {
        submissionDate: "202302",
        bank: "국민은행",
        productName: "상품C",
        sixMonthsRate: 3.6,
        twelveMonthsRate: 3.9,
        twentyFourMonthsRate: 4.1,
        thirtySixMonthsRate: 4.3,
      },
    ]);

    // 필터링된 데이터
    const filteredData = computed(() => {
      let filtered = tableData.value;

      // 검색어 필터
      if (searchQuery.value) {
        filtered = filtered.filter((item) =>
          item.bank.toLowerCase().includes(searchQuery.value.toLowerCase())
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
