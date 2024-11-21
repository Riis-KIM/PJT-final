<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">💱 환율 계산기</h1>
    <div class="card p-4 shadow-sm">
      <!-- 통화 선택 및 금액 입력 -->
      <div class="row g-3">
        <div class="col-md-4">
          <label for="fromCurrency" class="form-label">보낼 통화</label>
          <select 
            id="fromCurrency" 
            class="form-select" 
            v-model="fromCurrency"
          >
            <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency">
              {{ currency.cur_unit }} - {{ currency.cur_nm }}
            </option>
          </select>
        </div>

        <div class="col-md-4">
          <label for="toCurrency" class="form-label">받을 통화</label>
          <select 
            id="toCurrency" 
            class="form-select" 
            v-model="toCurrency"
          >
            <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency">
              {{ currency.cur_unit }} - {{ currency.cur_nm }}
            </option>
          </select>
        </div>

        <div class="col-md-4">
          <label for="amount" class="form-label">보낼 금액</label>
          <input
            id="amount"
            type="number"
            class="form-control"
            v-model.number="amount"
            placeholder="금액을 입력하세요"
          />
        </div>
      </div>

      <!-- 결과 표시 -->
      <div v-if="result" class="mt-4 text-center">
        <div class="alert alert-success">
          <h4 class="mb-0">
            {{ formatNumber(amount) }} {{ fromCurrency?.cur_unit }} = 
            {{ formatNumber(result) }} {{ toCurrency?.cur_unit }}
          </h4>
          <small class="text-muted">
            기준 환율: {{ fromCurrency?.cur_unit }} = {{ fromCurrency?.kftc_bkpr }}원
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeMount } from 'vue'
import axios from 'axios'

const currencies = ref([])
const fromCurrency = ref(null)
const toCurrency = ref(null)
const amount = ref(0)
const result = ref(null)

// 환율 데이터 가져오기
const fetchExchangeRates = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/exchange/')
    currencies.value = response.data
    
    // 기본값 설정 (USD와 KRW)
    fromCurrency.value = currencies.value.find(c => c.cur_unit === 'KRW')
    toCurrency.value = currencies.value.find(c => c.cur_unit === 'USD')
  } catch (error) {
    console.error('환율 데이터를 가져오는 중 오류 발생:', error)
  }
}

// 환율 계산 함수 수정
const calculateExchange = () => {
  if (!fromCurrency.value || !toCurrency.value || amount.value <= 0) {
    result.value = null
    return
  }

  const getAdjustedRate = (currency) => {
    const rate = parseFloat(currency.kftc_bkpr.replace(',', ''))
    // JPY와 IDR은 100단위이므로 100으로 나눔
    if (currency.cur_unit.includes('JPY') || currency.cur_unit.includes('IDR')) {
      return rate / 100
    }
    return rate
  }

  const fromRate = getAdjustedRate(fromCurrency.value)
  const toRate = getAdjustedRate(toCurrency.value)
  
  result.value = (amount.value * fromRate) / toRate
}

// 숫자 포맷팅 (천단위 쉼표)
const formatNumber = (num) => {
  return new Intl.NumberFormat().format(num)
}

// 입력값 변경 감지
watch([fromCurrency, toCurrency, amount], () => {
  calculateExchange()
}, { immediate: true })

onBeforeMount(() => {
  fetchExchangeRates()
})
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  border-radius: 15px;
  background: #fff;
}

.form-select, .form-control {
  border-radius: 8px;
}

.alert {
  border-radius: 8px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  .card {
    padding: 15px !important;
  }
}
</style>