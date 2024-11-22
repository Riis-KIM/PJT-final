<template>
  <div class="home">
    <h1 class="welcome-title">금융 앱에 오신 것을 환영합니다</h1>
    <p class="welcome-text">다양한 기능을 통해 효율적으로 금융 관리를 시작해보세요.</p>

    <!-- 추천 상품 배너 -->
    <div class="banner" @click="goToRecommendations">
      <h2>🎉 추천 금융 상품을 확인하세요! 🎉</h2>
      <p>나에게 꼭 맞는 금융 상품을 클릭 한 번으로 확인해보세요.</p>
      <button class="btn btn-primary btn-lg mt-3">추천 상품 보러가기</button>
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

<style scoped>
/* 홈 컨테이너 스타일 */
.home {
  text-align: center;
  padding: 40px 20px;
  background-color: #f9fafa;
}

/* 환영 메시지 스타일 */
.welcome-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.welcome-text {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

/* 배너 스타일 */
.banner {
  padding: 30px;
  background-color: #ffffff;
  border: 2px solid #ddd;
  border-radius: 15px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  max-width: 600px;
  margin: 0 auto;
}

.banner:hover {
  background-color: #f0f8ff;
  transform: translateY(-5px);
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.15);
}

/* 배너 텍스트 스타일 */
.banner h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #007bff;
  font-weight: bold;
}

.banner p {
  margin: 15px 0 0;
  font-size: 1.1rem;
  color: #555;
}

/* 버튼 스타일 */
.btn-primary {
  font-size: 1.2rem;
  padding: 10px 20px;
  background-color: #007bff;
  border: none;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>