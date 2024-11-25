<template>
  <div class="market-section">
    <!-- 코스피 차트 -->
    <div class="market-card">
      <h3>KOSPI</h3>
      <div class="chart-container">
        <Line 
          v-if="kospiChartData.datasets[0].data.length" 
          :data="kospiChartData" 
          :options="chartOptions" 
        />
      </div>
      <div class="price-info">
        <div class="current-price">{{ marketStore.marketInfo.kospi.price.toLocaleString() }}</div>
        <div :class="['change', marketStore.marketInfo.kospi.change > 0 ? 'up' : 'down']">
          {{ marketStore.marketInfo.kospi.change > 0 ? '+' : '' }}{{ marketStore.marketInfo.kospi.change }}%
        </div>
      </div>
    </div>

    <!-- 나스닥 차트 -->
    <div class="market-card">
      <h3>NASDAQ</h3>
      <div class="chart-container">
        <Line 
          v-if="nasdaqChartData.datasets[0].data.length" 
          :data="nasdaqChartData" 
          :options="chartOptions" 
        />
      </div>
      <div class="price-info">
        <div class="current-price">{{ marketStore.marketInfo.nasdaq.price.toLocaleString() }}</div>
        <div :class="['change', marketStore.marketInfo.nasdaq.change > 0 ? 'up' : 'down']">
          {{ marketStore.marketInfo.nasdaq.change > 0 ? '+' : '' }}{{ marketStore.marketInfo.nasdaq.change }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { useMarketStore } from '@/stores/market'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const marketStore = useMarketStore()

const kospiChartData = computed(() => ({
  labels: Array.from({ length: marketStore.marketInfo.kospi.last_1_month?.length || 0 }, (_, i) => i + 1),
  datasets: [{
    label: 'KOSPI',
    data: marketStore.marketInfo.kospi.last_1_month || [],
    borderColor: '#007AFF',
    tension: 0.1,
    fill: false
  }]
}))

const nasdaqChartData = computed(() => ({
  labels: Array.from({ length: marketStore.marketInfo.nasdaq.last_1_month?.length || 0 }, (_, i) => i + 1),
  datasets: [{
    label: 'NASDAQ',
    data: marketStore.marketInfo.nasdaq.last_1_month || [],
    borderColor: '#34C759',
    tension: 0.1,
    fill: false
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      display: false  // x축 숨기기
    },
    y: {
      beginAtZero: false,
      ticks: {
        callback: value => value.toLocaleString()
      }
    }
  }
}

onMounted(() => {
  marketStore.fetchMarketData()
})
</script>

<style scoped>
.market-section {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 2rem 0;
}

.market-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 400px;
}

.chart-container {
  height: 200px;
  margin: 1rem 0;
}

.price-info {
  text-align: center;
  margin-top: 1rem;
}

.current-price {
  font-size: 1.5rem;
  font-weight: bold;
}

.change {
  font-weight: 500;
  margin-top: 0.5rem;
}

.up { color: #28a745; }
.down { color: #dc3545; }
</style>