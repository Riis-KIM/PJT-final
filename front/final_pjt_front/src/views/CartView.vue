<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">구매 목록</h1>

    <!-- 보기 모드 버튼 -->
    <div class="d-flex justify-content-end mb-4 view-mode-buttons">
      <button
        class="btn btn-outline-green me-2"
        :class="{ active: viewMode === 'list' }"
        @click="viewMode = 'list'"
      >
        리스트로 보기
      </button>
      <button
        class="btn btn-outline-green"
        :class="{ active: viewMode === 'graph' }"
        @click="viewMode = 'graph'"
      >
        그래프로 보기
      </button>
    </div>

    <!-- 리스트 보기 -->
    <div v-if="viewMode === 'list'">
      <!-- 예금 목록 -->
      <div v-if="cart?.joined_deposits?.length" class="mb-5">
        <h2 class="fw-bold text-green text-center">예금 목록</h2>
        <table class="table table-bordered mt-3 cute-table">
          <thead>
            <tr>
              <th class="text-center">금융회사명</th>
              <th class="text-center">상품명</th>
              <th class="text-center text-green">최고금리</th>
              <th class="text-center">삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.joined_deposits" :key="item.fin_prdt_cd">
              <td class="text-center">{{ item.kor_co_nm }}</td>
              <td class="text-center">{{ item.fin_prdt_nm }}</td>
              <td class="text-center text-green fw-bold">
                {{ getMaxRate(item.options) }}%
              </td>
              <td class="text-center">
                <button
                  class="btn btn-light btn-sm cute-delete-btn"
                  @click="removeDeposit(item.fin_prdt_cd)"
                >
                  삭제
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 적금 목록 -->
      <div v-if="cart?.joined_savings?.length">
        <h2 class="fw-bold text-green text-center">적금 목록</h2>
        <table class="table table-bordered mt-3 cute-table">
          <thead>
            <tr>
              <th class="text-center">금융회사명</th>
              <th class="text-center">상품명</th>
              <th class="text-center text-green">최고금리</th>
              <th class="text-center">삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.joined_savings" :key="item.fin_prdt_cd">
              <td class="text-center">{{ item.kor_co_nm }}</td>
              <td class="text-center">{{ item.fin_prdt_nm }}</td>
              <td class="text-center text-green fw-bold">
                {{ getMaxRate(item.options) }}%
              </td>
              <td class="text-center">
                <button
                  class="btn btn-light btn-sm cute-delete-btn"
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
      <h2 class="fw-bold text-green text-center mb-4">가입 상품 금리 비교</h2>
      <div class="chart-wrapper">
        <canvas ref="graphCanvas"></canvas>
      </div>
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
  Legend,
} from "chart.js";

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const cart = ref(null);
const viewMode = ref("list");
const chartInstance = ref(null);
const graphCanvas = ref(null);

const fetchCart = async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.get("/accounts/custom/myproducts/", {
      headers: { Authorization: `Token ${token}` },
    });
    cart.value = response.data;
  } catch (error) {
    console.error("데이터 로드 실패:", error);
  }
};

const removeDeposit = async (fin_prdt_cd) => {
  const isConfirmed = window.confirm("정말 이 예금 상품을 삭제하시겠습니까?");
  if (!isConfirmed) return;

  try {
    const token = localStorage.getItem("token");
    await axios.post(`/api/v1/deposits/${fin_prdt_cd}/join/`, {}, {
      headers: { Authorization: `Token ${token}` },
    });
    alert("삭제되었습니다");
    await fetchCart();
  } catch (error) {
    console.error("예금 삭제 실패:", error);
    alert("삭제 중 오류가 발생했습니다. 다시 시도해주세요.");
  }
};

const removeSaving = async (fin_prdt_cd) => {
  const isConfirmed = window.confirm("정말 이 적금 상품을 삭제하시겠습니까?");
  if (!isConfirmed) return;

  try {
    const token = localStorage.getItem("token");
    await axios.post(`/api/v1/savings/${fin_prdt_cd}/join/`, {}, {
      headers: { Authorization: `Token ${token}` },
    });
    alert("삭제되었습니다");
    await fetchCart();
  } catch (error) {
    console.error("적금 삭제 실패:", error);
    alert("삭제 중 오류가 발생했습니다. 다시 시도해주세요.");
  }
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
  const depositBasicRates = cart.value?.joined_deposits?.map((item) =>
    item.options ? Math.min(...item.options.map((opt) => opt.intr_rate || 0)) : 0
  );
  const depositMaxRates = cart.value?.joined_deposits?.map((item) =>
    item.options ? Math.max(...item.options.map((opt) => opt.intr_rate2 || 0)) : 0
  );

  const savingLabels = cart.value?.joined_savings?.map((item) => item.fin_prdt_nm) || [];
  const savingBasicRates = cart.value?.joined_savings?.map((item) =>
    item.options ? Math.min(...item.options.map((opt) => opt.intr_rate || 0)) : 0
  );
  const savingMaxRates = cart.value?.joined_savings?.map((item) =>
    item.options ? Math.max(...item.options.map((opt) => opt.intr_rate2 || 0)) : 0
  );

  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [...depositLabels, ...savingLabels],
      datasets: [
        {
          label: "저축 금리",
          data: [...depositBasicRates, ...savingBasicRates],
          backgroundColor: "rgba(40, 167, 69, 0.8)",
          borderColor: "rgba(40, 167, 69, 1)",
          borderWidth: 1,
        },
        {
          label: "최고 금리",
          data: [...depositMaxRates, ...savingMaxRates],
          backgroundColor: "rgba(75, 192, 192, 0.8)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top" },
      },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true },
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
.text-green {
  color: #28a745;
}

.btn-outline-green {
  border: 1px solid #28a745;
  color: #28a745;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-outline-green.active,
.btn-outline-green:hover {
  background: #28a745;
  color: white;
}

.cute-delete-btn {
  border-radius: 8px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

.cute-delete-btn:hover {
  background: #ffc9c9;
  color: #721c24;
}

.cute-table th {
  background-color: #f8f9fa;
  color: #28a745;
  text-transform: uppercase;
  font-size: 0.85rem;
}

.cute-table tbody tr:hover {
  background-color: #f1f3f5;
}

.graph-container {
  position: relative;
  height: 600px; /* 높이 확장 */
  width: 1500px; /* 너비 확장 */
  margin: 0 auto;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.chart-wrapper {
  overflow-x: auto;
}

canvas {
  display: block;
  width: 1400px; /* 캔버스와 컨테이너 크기 동기화 */
  height: 500px;
  margin: auto;
}
</style>
