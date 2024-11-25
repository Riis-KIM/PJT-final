// stores/market.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMarketStore = defineStore('market', () => {
  const marketInfo = ref({
    kospi: { 
      price: 0, 
      change: 0,
      last_1_month: []
    },
    nasdaq: { 
      price: 0, 
      change: 0,
      last_1_month: []
    }
  })

  const chartData = computed(() => ({
    kospi: {
      labels: marketInfo.value.kospi.last_1_month?.map(item => item.date),
      datasets: [{
        label: 'KOSPI',
        data: marketInfo.value.kospi.last_1_month?.map(item => item.price),
        borderColor: '#007AFF',
        tension: 0.1,
        fill: false
      }]
    },
    nasdaq: {
      labels: marketInfo.value.nasdaq.last_1_month?.map(item => item.date),
      datasets: [{
        label: 'NASDAQ',
        data: marketInfo.value.nasdaq.last_1_month?.map(item => item.price),
        borderColor: '#34C759',
        tension: 0.1,
        fill: false
      }]
    }
  }))

  const fetchMarketData = () => {
    return axios.get('/exchange/market-data/')
      .then(response => {
        marketInfo.value = response.data
      })
  }

  return {
    marketInfo,
    chartData,
    fetchMarketData
  }
})