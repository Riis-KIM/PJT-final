<template>
  <div class="container mt-5">
    <!-- 환율 계산기 헤더 -->
    <section class="header-section mb-4">
      <h1 class="fw-bold mb-2 section-title">환율 계산기</h1>
      <p class="lead section-subtitle">간편하게 환율을 계산해보세요</p>
    </section>

    <!-- 환율 계산기 카드 -->
    <div class="card p-4 shadow-sm exchange-card">
      <div class="row g-3">
        <!-- 보낼 통화 선택 -->
        <div class="col-md-4">
          <label for="fromCurrency" class="form-label fw-semibold">보낼 통화</label>
          <select 
            id="fromCurrency" 
            class="form-select form-control-lg" 
            v-model="fromCurrency"
          >
            <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency">
              {{ currency.cur_unit }} - {{ currency.cur_nm }}
            </option>
          </select>
        </div>

        <!-- 받을 통화 선택 -->
        <div class="col-md-4">
          <label for="toCurrency" class="form-label fw-semibold">받을 통화</label>
          <select 
            id="toCurrency" 
            class="form-select form-control-lg" 
            v-model="toCurrency"
          >
            <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency">
              {{ currency.cur_unit }} - {{ currency.cur_nm }}
            </option>
          </select>
        </div>

        <!-- 보낼 금액 입력 -->
        <div class="col-md-4">
          <label for="amount" class="form-label fw-semibold">보낼 금액</label>
          <input
            id="amount"
            type="number"
            class="form-control form-control-lg"
            v-model.number="amount"
            placeholder="금액을 입력하세요"
          />
        </div>
      </div>

      <!-- 계산 결과 -->
      <div v-if="result" class="mt-4">
        <div class="result-card p-4 shadow">
          <h3 class="result-text fw-bold mb-3 text-center">
            {{ formatNumber(amount) }} {{ fromCurrency?.cur_unit }} = 
            {{ formatNumber(result) }} {{ toCurrency?.cur_unit }}
          </h3>
          <div class="d-flex justify-content-between align-items-center text-muted">
            <p class="mb-0">기준 환율: 1 {{ toCurrency?.cur_unit }} = {{ toCurrency?.kftc_bkpr }}원</p>
            <small>업데이트: 실시간 기준</small>
          </div>
        </div>
      </div>
    </div>

    <!-- 주요 환율 정보 테이블 -->
    <div class="major-currencies mt-4">
      <h4 class="fw-bold mb-3">주요 국가 환율 정보 <small class="text-muted">(KRW 기준)</small></h4>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>통화명</th>
            <th>매매기준율</th>
            <th>살 때</th>
            <th>팔 때</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="code in orderedCountryCodes" :key="code">
            <td>{{ findCurrency(code)?.cur_nm || "정보 없음" }}</td>
            <td>{{ findCurrency(code)?.deal_bas_r || "정보 없음" }}</td>
            <td>{{ findCurrency(code)?.tts || "정보 없음" }}</td>
            <td>{{ findCurrency(code)?.ttb || "정보 없음" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';

const currencies = ref([]);
const fromCurrency = ref(null);
const toCurrency = ref(null);
const amount = ref(0);
const result = ref(null);

// 주요 국가 코드 순서
const orderedCountryCodes = [
  "USD", // 미국
  "JPY(100)", // 일본
  "EUR", // 유럽연합
  "CNH", // 중국
  "GBP", // 영국
  "AUD", // 호주
  "CAD", // 캐나다
  "NZD", // 뉴질랜드
  "THB", // 태국
  "HKD", // 홍콩
  "IDR(100)", // 인도네시아
  "SGD", // 싱가포르
];

// 환율 데이터 가져오기
const fetchExchangeRates = () => {
  axios.get('http://127.0.0.1:8000/exchange/')
    .then((response) => {
      currencies.value = response.data;
      fromCurrency.value = currencies.value.find((c) => c.cur_unit === 'KRW');
      toCurrency.value = currencies.value.find((c) => c.cur_unit === 'USD');
      calculateExchange();
    })
    .catch((err) => console.error('환율 데이터를 가져오는 중 오류 발생:', err));
};

// 특정 통화 코드로 데이터 찾기
const findCurrency = (code) => currencies.value.find(currency => currency.cur_unit === code);

// 환율 계산 함수
const calculateExchange = () => {
  if (!fromCurrency.value || !toCurrency.value || amount.value <= 0) {
    result.value = null;
    return;
  }

  const getAdjustedRate = (currency) => {
    const rate = parseFloat(currency.kftc_bkpr.replace(',', ''));
    return currency.cur_unit.includes('JPY') || currency.cur_unit.includes('IDR') ? rate / 100 : rate;
  };

  const fromRate = getAdjustedRate(fromCurrency.value);
  const toRate = getAdjustedRate(toCurrency.value);

  result.value = (amount.value * fromRate) / toRate;
};

// 숫자 포맷팅 함수
const formatNumber = (num) => new Intl.NumberFormat().format(num);

// 값 변경 감지
watch([fromCurrency, toCurrency, amount], calculateExchange);

onMounted(() => {
  fetchExchangeRates();
});
</script>

<style scoped>
/* 헤더 스타일 */
.header-section {
  text-align: left;
}

.section-title {
  font-size: 2.2rem;
  color: #343a40;
}

.section-subtitle {
  font-size: 1rem;
  color: #868e96;
}

/* 카드 스타일 */
.exchange-card {
  border-radius: 15px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
}

/* 결과 카드 */
.result-card {
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 15px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.result-text {
  font-size: 1.5rem;
  color: #495057;
}

/* 테이블 스타일 */
.table {
  text-align: center;
}

.table th,
.table td {
  vertical-align: middle;
}
</style>
