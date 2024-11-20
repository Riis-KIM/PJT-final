<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">🔍 금리 검색</h1>

    <!-- 검색 및 필터 기능 -->
    <div class="d-flex justify-content-between mb-3">
      <div class="w-50">
        <label for="bankFilter" class="form-label">은행 선택</label>
        <input
          id="bankFilter"
          type="text"
          class="form-control"
          placeholder="은행명을 입력하세요"
          v-model="searchQuery"
        />
      </div>
      <div class="d-flex align-items-end">
        <div class="btn-group">
          <button 
            class="btn" 
            :class="productType === 'deposit' ? 'btn-primary' : 'btn-outline-primary'"
            @click="productType = 'deposit'"
          >
            예금
          </button>
          <button 
            class="btn" 
            :class="productType === 'saving' ? 'btn-primary' : 'btn-outline-primary'"
            @click="productType = 'saving'"
          >
            적금
          </button>
        </div>
      </div>
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
          <th @click="sortTable('maxRate')" style="cursor: pointer;">
            최고금리
          </th>
          <th>6개월</th>
          <th>12개월</th>
          <th>24개월</th>
          <th>36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in filteredData" :key="item.fin_prdt_cd">
          <td>{{ item.kor_co_nm }}</td>
          <td>{{ item.fin_prdt_nm }}</td>
          <td>{{ getMaxRate(item.options) }}%</td>
          <td>{{ getTermRate(item.options, 6) }}</td>
          <td>{{ getTermRate(item.options, 12) }}</td>
          <td>{{ getTermRate(item.options, 24) }}</td>
          <td>{{ getTermRate(item.options, 36) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const sortKey = ref('')
const sortOrder = ref(1)
const tableData = ref([])
const productType = ref('deposit') // 'deposit' 또는 'saving'

// 특정 기간의 금리를 반환하는 함수
const getTermRate = (options, term) => {
  const option = options?.find(opt => opt.save_trm === term)
  if (!option || option.intr_rate === null) return '-'
  return `${option.intr_rate}%`
}

// 최고 금리를 반환하는 함수
const getMaxRate = (options) => {
  if (!options || options.length === 0) return '-'
  const rates = options.map(opt => opt.intr_rate).filter(rate => rate !== null)
  if (rates.length === 0) return '-'
  return Math.max(...rates).toFixed(2)
}

// API 호출
const fetchData = async () => {
  try {
    const [depositResponse, savingResponse] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/v1/deposits/'),
      axios.get('http://127.0.0.1:8000/api/v1/savings/')
    ])
    
    tableData.value = {
      deposit: depositResponse.data,
      saving: savingResponse.data
    }
  } catch (error) {
    console.error('데이터를 가져오는 중 오류 발생:', error)
  }
}

// 필터링된 데이터
const filteredData = computed(() => {
  let filtered = tableData.value[productType.value] || []

  if (searchQuery.value) {
    filtered = filtered.filter((item) =>
      item.kor_co_nm.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (sortKey.value) {
    filtered = filtered.sort((a, b) => {
      let aValue = a[sortKey.value]
      let bValue = b[sortKey.value]
      
      // 최고금리로 정렬하는 경우
      if (sortKey.value === 'maxRate') {
        aValue = parseFloat(getMaxRate(a.options))
        bValue = parseFloat(getMaxRate(b.options))
      }

      if (aValue < bValue) return -1 * sortOrder.value
      if (aValue > bValue) return 1 * sortOrder.value
      return 0
    })
  }

  return filtered
})

// 정렬 함수
const sortTable = (key) => {
  if (sortKey.value === key) {
    sortOrder.value *= -1
  } else {
    sortKey.value = key
    sortOrder.value = 1
  }
}

onMounted(() => {
  fetchData()
})
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

.btn-group {
  margin-bottom: 1rem;
}
</style>