<template>
  <div class="login-container">
    <h2 class="text-center">로그인</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="username" class="form-label">사용자 이름</label>
        <input
          type="text"
          class="form-control"
          id="username"
          v-model="username"
          placeholder="사용자 이름을 입력하세요"
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
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios({
          method: "post",
          url: "http://127.0.0.1:8000/api/v1/login/",
          headers: {
            "Content-Type": "application/json",
          },
          data: {
            username: this.username,
            password: this.password,
          },
        });

        if (response.status === 200) {
          alert("로그인 성공!");
          localStorage.setItem("isLoggedIn", true);
          localStorage.setItem("currentUser", this.username);
          this.$router.push("/");
        }
      } catch (error) {
        console.error("로그인 중 오류 발생:", error);
        alert("로그인에 실패했습니다. 사용자 이름과 비밀번호를 확인하세요.");
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
