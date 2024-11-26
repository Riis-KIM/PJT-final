<template>
  <div class="container mt-5">
    <h1 class="fw-bold mb-4 text-center">상품 상세정보</h1>
    <div v-if="product" class="card shadow-lg p-4">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">{{ product.fin_prdt_nm }}</h2>
        <p class="card-text">
          <strong>금융회사명:</strong> {{ product.kor_co_nm }}
        </p>
        <p class="card-text">
          <strong>가입제한:</strong> {{ product.join_deny === 1 ? "개인" : "법인" }}
        </p>
        <p class="card-text"><strong>우대조건:</strong></p>
        <ul class="list-group mb-3">
          <li
            class="list-group-item"
            v-for="condition in formatConditions(product.spcl_cnd)"
            :key="condition"
          >
            {{ condition }}
          </li>
        </ul>
        <p class="card-text">
          <strong>가입방법:</strong> {{ product.join_way }}
        </p>
        <!-- 구매 목록에 추가 버튼 -->
        <div class="text-center mt-4">
          <button class="btn btn-primary btn-lg" @click="addToCart">
            가입 목록에 추가
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-center mt-5">
      <p class="text-muted">상품 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { useProductStore } from "@/stores/productStore"; // Pinia 스토어 사용
import axios from "axios";

const route = useRoute();
const productStore = useProductStore();
const product = ref(null); // 선택된 상품 데이터를 저장
const type = ref(route.params.type); // type 값을 route에서 받아옴

// 우대 조건 포맷팅 함수
const formatConditions = (conditions) => {
  if (!conditions) return ["없음"];
  return conditions.split("\n").filter((line) => line.trim() !== "");
};

// 가입 경로를 설정하는 함수
const getJoinUrl = () => {
  if (type.value === "deposit") {
    return `/api/v1/deposits/${product.value.fin_prdt_cd}/join/`;
  } else if (type.value === "saving") {
    return `/api/v1/savings/${product.value.fin_prdt_cd}/join/`;
  } else {
    throw new Error("잘못된 상품 유형입니다."); // 잘못된 type 처리
  }
};

// 인기도 업데이트 경로 설정 함수
const getPopularityUrl = () => {
  if (type.value === "deposit") {
    return `/api/v1/deposits/${product.value.fin_prdt_cd}/popularity/`
  } else if (type.value === "saving") {
    return `/api/v1/savings/${product.value.fin_prdt_cd}/popularity/`
  }
}

// 구매 목록에 추가
const addToCart = () => {
  // 구매 요청
  axios({
    method: 'post',
    url: getJoinUrl(),
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`
    }
  })
    .then((res) => {
      const joined = res.data.joined
      if (joined) {
        // 구매 성공 시 인기도 업데이트 (purchase 카운트 증가)
        axios({
          method: 'put',
          url: getPopularityUrl(),
          data: { purchase: true },
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`
          }
        })
        alert("구매 목록에 추가되었습니다!")
      } else {
        alert("이미 구매 목록에 추가된 상품입니다!")
      }
    })
    .catch((err) => {
      console.error("구매 목록에 추가하는 중 오류 발생:", err)
      alert("구매 목록에 추가하지 못했습니다. 다시 시도해주세요.")
    })
}

// 새로고침 시 데이터를 복원하기 위한 함수
const loadProductFromLocalStorage = () => {
  const storedProduct = localStorage.getItem("selectedProduct");
  if (storedProduct) {
    return JSON.parse(storedProduct);
  }
  return null;
};

const startTime = ref(0)  // 페이지 접속 시 시간
onMounted(() => {
  console.log(type.value)
  const storedProduct = loadProductFromLocalStorage();

  // Pinia 스토어에서 데이터를 가져오거나 localStorage에서 복원
  product.value = productStore.getProduct(route.params.id) || storedProduct;

  // localStorage에 데이터 저장
  if (product.value) {
    localStorage.setItem("selectedProduct", JSON.stringify(product.value));
  }
  // 페이지 진입 시간 기록
  startTime.value = Date.now()
});

onUnmounted(() => {
  const stayTime = (Date.now() - startTime.value) / 1000 // 초 단위로 변환
  console.log(stayTime)
  if (stayTime >= 10) {
    axios({
      method: 'put',
      url: `/api/v1/${type.value}s/${product.value.fin_prdt_cd}/popularity/`,
      data: { view_time: true },
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
  }
})

</script>

<style scoped>
.container {
  margin-top: 2rem;
}

/* 카드 스타일 */
.container {
  margin-top: 2rem;
}

.card {
  border-radius: 10px;
  background-color: white; /* 연한 초록색 배경 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.75rem;
  font-weight: bold;
  color: black; /* 메인 초록색 */
}

.card-text {
  font-size: 1.1rem;
  color: #333;
}

.list-group-item {
  font-size: 1rem;
  background-color: #f8f9fa;
  border-left: 4px solid #28a745; /* 초록색 강조 */
}

.btn-primary {
  background-color: #28a745; /* 메인 초록색 */
  border: none;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
}

.btn-primary:hover {
  background-color: #218838; /* 조금 더 짙은 초록색 */
  transition: background-color 0.3s ease;
}
</style>
