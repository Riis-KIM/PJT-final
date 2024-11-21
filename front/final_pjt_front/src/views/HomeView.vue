<template>
  <div class="home">
    <h1>금융 앱에 오신 것을 환영합니다</h1>
    <p>다양한 기능을 통해 효율적으로 금융 관리를 시작해보세요.</p>

    <!-- 추천 상품 배너 -->
    <div class="banner" @click="goToRecommendations">
      <h2>🎉 추천 상품을 확인하세요! 🎉</h2>
      <p>나에게 맞는 금융 상품을 클릭 한 번으로 확인할 수 있습니다!</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  methods: {
    goToRecommendations() {
      // 추천 상품 페이지로 이동
      this.$router.push({ name: "ProductRecommendations" });
    },
  },
};
</script>

<style>
.home {
  text-align: center;
  padding: 20px;
}

.banner {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.banner:hover {
  background-color: #e9ecef;
  transform: translateY(-5px);
}

.banner h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #007bff;
}

.banner p {
  margin: 10px 0 0;
  font-size: 1rem;
  color: #495057;
}
</style>
