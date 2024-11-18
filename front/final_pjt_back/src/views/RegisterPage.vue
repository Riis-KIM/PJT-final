<template>
  <div class="register-container">
    <h2 class="text-center">회원가입</h2>
    <form @submit.prevent="handleRegister">
      <!-- 이메일 입력 -->
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

      <!-- 비밀번호 입력 -->
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

      <!-- 회원가입 버튼 -->
      <button type="submit" class="btn btn-primary w-100">회원가입</button>
    </form>

    <!-- 로그인 링크 -->
    <p class="text-center mt-3">
      이미 계정이 있으신가요? <router-link to="/login">로그인</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: "RegisterPage",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    /**
     * 회원가입 처리
     */
    async handleRegister() {
      // 필드 검증
      if (!this.email || !this.password) {
        alert("이메일과 비밀번호를 모두 입력하세요.");
        return;
      }

      // 유효성 검사 추가 (예: 비밀번호 최소 길이)
      if (this.password.length < 6) {
        alert("비밀번호는 최소 6자 이상이어야 합니다.");
        return;
      }

      // 사용자 데이터 객체 생성
      const userData = { email: this.email, password: this.password };

      // localStorage에 사용자 데이터를 저장
      try {
        let users = localStorage.getItem("users");
        users = users ? JSON.parse(users) : []; // 기존 사용자 목록 가져오기

        // 이메일 중복 체크
        const isEmailTaken = users.some((user) => user.email === this.email);
        if (isEmailTaken) {
          alert("이미 사용 중인 이메일입니다.");
          return;
        }

        // 사용자 추가 후 저장
        users.push(userData);
        localStorage.setItem("users", JSON.stringify(users));

        // 성공 메시지 및 로그인 페이지로 이동
        alert("회원가입 성공! 이제 로그인하세요.");
        this.$router.push("/login");
      } catch (error) {
        console.error("회원가입 중 오류 발생:", error);
        alert("회원가입 중 문제가 발생했습니다. 다시 시도해주세요.");
      }
    },
  },
};
</script>

<style scoped>
.register-container {
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
