<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">💱 환율 계산기</h1>

    <!-- 통화 선택 및 금액 입력 -->
    <div class="row mb-3">
      <div class="col-md-4">
        <label for="fromCurrency" class="form-label">보낼 통화</label>
        <select id="fromCurrency" class="form-select" v-model="fromCurrency">
          <option v-for="(rate, currency) in rates" :key="currency" :value="currency">
            {{ currency }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <label for="toCurrency" class="form-label">받을 통화</label>
        <select id="toCurrency" class="form-select" v-model="toCurrency">
          <option v-for="(rate, currency) in rates" :key="currency" :value="currency">
            {{ currency }}
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
    <div class="mt-3">
      <button @click="calculateExchange" class="btn btn-primary">계산하기</button>
      <p class="mt-3" v-if="result !== null">
        {{ amount }} {{ fromCurrency }} → {{ result }} {{ toCurrency }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ExchangeCalculator",
  data() {
    return {
      rates: {}, // 환율 데이터
      fromCurrency: "USD", // 기본 통화
      toCurrency: "KRW", // 변환할 통화
      amount: 0, // 변환 금액
      result: null, // 계산 결과
    };
  },
  methods: {
    // 환율 데이터 가져오기
    async fetchRates() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/exchange-rates/");
        this.rates = response.data.rates; // API에서 받은 환율 데이터
      } catch (error) {
        console.error("환율 데이터를 가져오는 중 오류 발생:", error);
      }
    },
    // 환율 계산
    calculateExchange() {
      if (this.amount <= 0 || !this.rates[this.fromCurrency] || !this.rates[this.toCurrency]) {
        alert(" ");
        return;
      }
      const rate = this.rates[this.toCurrency] / this.rates[this.fromCurrency];
      this.result = (this.amount * rate).toFixed(2); // 결과를 소수점 둘째 자리까지 표시
    },
  },
  mounted() {
    this.fetchRates(); // 컴포넌트 마운트 시 환율 데이터 가져오기
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

select,
input {
  text-align: center;
}

button {
  width: 100%;
  margin-top: 20px;
}
</style>
