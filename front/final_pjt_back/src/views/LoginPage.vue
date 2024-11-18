<template>
  <div class="login-container">
    <h2 class="text-center">로그인</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <input
          type="email"
          class="form-control"
          id="email"
          v-model="email"
          placeholder="이메일을 입력하세요"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="password"
          placeholder="비밀번호를 입력하세요"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary w-100">로그인</button>
      <p class="text-center mt-3">
  계정이 없으신가요? <router-link to="/register">회원가입</router-link>
</p>
    </form>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
      // 실제 API 요청을 여기에 추가
      if (this.email === "test@example.com" && this.password === "password") {
        alert("로그인 성공!");
        localStorage.setItem("isLoggedIn", true);
        this.$router.push("/"); // 로그인 후 홈으로 이동
      } else {
        alert("로그인 실패: 이메일 또는 비밀번호를 확인하세요.");
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
}
</style>
