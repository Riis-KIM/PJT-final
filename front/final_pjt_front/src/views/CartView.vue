<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">구매 목록</h1>

    <!-- 보기 모드 버튼 -->
    <div class="d-flex justify-content-end mb-4 view-mode-buttons">
      <button
        class="btn btn-outline-primary me-2 view-mode-btn"
        :class="{ active: viewMode === 'list' }"
        @click="viewMode = 'list'"
      >
        리스트로 보기
      </button>
      <button
        class="btn btn-outline-primary view-mode-btn"
        :class="{ active: viewMode === 'graph' }"
        @click="viewMode = 'graph'"
      >
        그래프로 보기
      </button>
    </div>

    <!-- 리스트 보기 -->
    <div v-if="viewMode === 'list'">
      <div v-if="cart?.joined_deposits?.length" class="mb-5">
        <h2 class="fw-bold text-center">예금 목록</h2>
        <table class="table table-striped table-hover mt-3">
          <thead>
            <tr>
              <th class="text-center">금융회사명</th>
              <th class="text-center">상품명</th>
              <th class="text-center text-success">최고금리</th>
              <th class="text-center">삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.joined_deposits" :key="item.fin_prdt_cd">
              <td class="text-center">{{ item.kor_co_nm }}</td>
              <td class="text-center">{{ item.fin_prdt_nm }}</td>
              <td class="text-center text-success fw-bold">
                {{ getMaxRate(item.options) }}%
              </td>
              <td class="text-center">
                <button
                  class="btn btn-danger btn-sm"
                  @click="removeDeposit(item.fin_prdt_cd)"
                >
                  삭제
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="cart?.joined_savings?.length">
        <h2 class="fw-bold text-center">적금 목록</h2>
        <table class="table table-striped table-hover mt-3">
          <thead>
            <tr>
              <th class="text-center">금융회사명</th>
              <th class="text-center">상품명</th>
              <th class="text-center text-success">최고금리</th>
              <th class="text-center">삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.joined_savings" :key="item.fin_prdt_cd">
              <td class="text-center">{{ item.kor_co_nm }}</td>
              <td class="text-center">{{ item.fin_prdt_nm }}</td>
              <td class="text-center text-success fw-bold">
                {{ getMaxRate(item.options) }}%
              </td>
              <td class="text-center">
                <button
                  class="btn btn-danger btn-sm"
                  @click="removeSaving(item.fin_prdt_cd)"
                >
                  삭제
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 그래프 보기 -->
    <div v-else class="graph-container">
      <h2 class="fw-bold text-center text-info mb-4">금융상품 최고 금리 비교</h2>
      <canvas ref="graphCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from "vue";
import axios from "axios";
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
} from "chart.js";

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip);

const cart = ref(null);
const viewMode = ref("list");
const chartInstance = ref(null);
const graphCanvas = ref(null);

const fetchCart = () => {
  const token = localStorage.getItem("token");
  axios
    .get("/accounts/custom/myproducts/", {
      headers: { Authorization: `Token ${token}` },
    })
    .then((response) => {
      cart.value = response.data;
    })
    .catch((error) => console.error("Error fetching cart:", error));
};

const getMaxRate = (options) => {
  const rates =
    options?.map((opt) => opt.intr_rate).filter((rate) => rate !== null) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : "-";
};

const renderGraph = async () => {
  await nextTick();
  const ctx = graphCanvas.value?.getContext("2d");
  if (!ctx) return;

  if (chartInstance.value) chartInstance.value.destroy();

  const depositLabels = cart.value?.joined_deposits?.map((item) => item.fin_prdt_nm) || [];
  const depositData = cart.value?.joined_deposits?.map((item) =>
    item.options ? Math.max(...item.options.map((opt) => opt.intr_rate || 0)) : 0
  );

  const savingLabels = cart.value?.joined_savings?.map((item) => item.fin_prdt_nm) || [];
  const savingData = cart.value?.joined_savings?.map((item) =>
    item.options ? Math.max(...item.options.map((opt) => opt.intr_rate || 0)) : 0
  );

  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [...depositLabels, ...savingLabels],
      datasets: [
        {
          label: "최고 금리 (%)",
          data: [...depositData, ...savingData],
          backgroundColor: "rgba(54, 162, 235, 0.5)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          enabled: true,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
        x: {
          ticks: {
            maxRotation: 45,
            minRotation: 0,
            autoSkip: true,
          },
        },
      },
    },
  });
};

watch(viewMode, async (mode) => {
  if (mode === "graph") await renderGraph();
});

onMounted(() => {
  fetchCart();
});
</script>

<style scoped>
.graph-container {
  position: relative;
  height: 500px;
  width: 100%;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

canvas {
  display: block;
  margin: auto;
}

.table {
  text-align: center;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.05);
}

h2 {
  color: #343a40;
}
</style>
