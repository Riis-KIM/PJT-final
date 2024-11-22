<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4">🛒 구매 목록</h1>

    <!-- 보기 모드 버튼 -->
    <div class="d-flex justify-content-end mb-4">
      <button
        class="btn btn-outline-primary me-2"
        :class="{ active: viewMode === 'list' }"
        @click="viewMode = 'list'"
      >
        리스트로 보기
      </button>
      <button
        class="btn btn-outline-primary"
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
        <h2 class="fw-bold text-center">예금 목록</h2>
        <table class="table table-striped table-hover mt-3">
          <thead class="table-dark">
            <tr>
              <th class="text-center" style="width: 25%;">금융회사명</th>
              <th class="text-center" style="width: 40%;">상품명</th>
              <th class="text-center" style="width: 20%;">최고금리</th>
              <th class="text-center" style="width: 15%;">삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.joined_deposits" :key="item.fin_prdt_cd">
              <td class="text-center">{{ item.kor_co_nm }}</td>
              <td class="text-center">{{ item.fin_prdt_nm }}</td>
              <td class="text-center">{{ item.options ? getMaxRate(item.options) + "%" : "-" }}</td>
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

      <!-- 적금 목록 -->
      <div v-if="cart?.joined_savings?.length">
        <h2 class="fw-bold text-center">적금 목록</h2>
        <table class="table table-striped table-hover mt-3">
          <thead class="table-dark">
            <tr>
              <th class="text-center" style="width: 25%;">금융회사명</th>
              <th class="text-center" style="width: 40%;">상품명</th>
              <th class="text-center" style="width: 20%;">최고금리</th>
              <th class="text-center" style="width: 15%;">삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart.joined_savings" :key="item.fin_prdt_cd">
              <td class="text-center">{{ item.kor_co_nm }}</td>
              <td class="text-center">{{ item.fin_prdt_nm }}</td>
              <td class="text-center">{{ item.options ? getMaxRate(item.options) + "%" : "-" }}</td>
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
    <div v-else>
      <canvas ref="graphCanvas" width="800" height="600"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from "vue";
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

// Chart.js 구성 요소 등록
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const cart = ref(null);
const viewMode = ref("list"); // 보기 모드: "list" 또는 "graph"
const chartInstance = ref(null); // Chart.js 인스턴스
const graphCanvas = ref(null); // 그래프 캔버스 참조

// API를 호출하여 구매 목록 가져오기
const fetchCart = () => {
  const token = localStorage.getItem("token")
  axios({
    method: 'get',
    url: '/accounts/custom/myproducts/',
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then((response) => {
      cart.value = response.data
    })
    .catch((err) => {
      console.error("구매 목록을 가져오는 중 오류 발생:", err)
    })
}

// 최고 금리를 반환하는 함수
const getMaxRate = (options) => {
  const rates = options?.map((opt) => opt.intr_rate).filter((rate) => rate !== null) || [];
  return rates.length ? Math.max(...rates).toFixed(2) : "-";
};

// 예금 삭제
const removeDeposit = (productId) => {
  const token = localStorage.getItem("token")
  axios({
    method: 'post',
    url: `/api/v1/deposits/${productId}/join/`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then(() => {
      cart.value.joined_deposits = cart.value.joined_deposits.filter(
        (item) => item.fin_prdt_cd !== productId
      )
      alert("예금 상품이 삭제되었습니다.")
    })
    .catch((err) => {
      console.error("예금 항목을 제거하는 중 오류 발생:", err)
    })
}

// 적금 삭제
const removeSaving = (productId) => {
  const token = localStorage.getItem("token")
  axios({
    method: 'post',
    url: `/api/v1/savings/${productId}/join/`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then(() => {
      cart.value.joined_savings = cart.value.joined_savings.filter(
        (item) => item.fin_prdt_cd !== productId
      )
      alert("적금 상품이 삭제되었습니다.")
    })
    .catch((err) => {
      console.error("적금 항목을 제거하는 중 오류 발생:", err)
    })
}

// 그래프 렌더링
const renderGraph = async () => {
  await nextTick(); // DOM 업데이트 후 실행
  const ctx = graphCanvas.value?.getContext("2d");
  if (!ctx) {
    console.error("그래프 캔버스를 찾을 수 없습니다.");
    return;
  }

  // 기존 그래프 제거
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }

  // 데이터 준비
  const depositLabels = cart.value?.joined_deposits?.map((item) => item.fin_prdt_nm) || [];
  const depositData = cart.value?.joined_deposits?.map((item) => {
    return item.options ? Math.max(...item.options.map((opt) => opt.intr_rate || 0)) : 0;
  }) || [];

  const savingLabels = cart.value?.joined_savings?.map((item) => item.fin_prdt_nm) || [];
  const savingData = cart.value?.joined_savings?.map((item) => {
    return item.options ? Math.max(...item.options.map((opt) => opt.intr_rate || 0)) : 0;
  }) || [];

  const labels = [...depositLabels, ...savingLabels];
  const data = [...depositData, ...savingData];

  // 그래프 생성
  chartInstance.value = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "최고 금리 (%)",
          data: data,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};

// 보기 모드 변경 시 그래프 렌더링
watch(viewMode, async (newMode) => {
  if (newMode === "graph") {
    await renderGraph();
  }
});

// 컴포넌트 마운트 시 구매 목록 가져오기
onMounted(() => {
  fetchCart();
});
</script>

<style scoped>
.container {
  margin-top: 2rem;
}

.table {
  text-align: center;
}

th,
td {
  vertical-align: middle;
}

button {
  font-size: 0.9rem;
}

canvas {
  margin: 0 auto;
  display: block;
}
</style>
