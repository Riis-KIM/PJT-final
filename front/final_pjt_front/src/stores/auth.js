// store/auth.js
import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  const token = ref(null);
  const user = ref(null);

  const isAuthenticated = computed(() => {
    return token.value !== null;
  });

  // 회원가입
  const register = function (payload) {
    axios({
      method: 'post',
      url: '/accounts/signup/',
      data: {
        username: payload.username,
        password1: payload.password1,
        password2: payload.password2,
        email: payload.email,
      },
    })
      .then(() => {
        router.push({ name: 'login' });
        alert('회원가입이 완료되었습니다.')
      })
      .catch((err) => {
        console.error(err);
        if (err.response?.data) {
          const errorMessage = Object.values(err.response.data).flat().join('\n');
          alert(errorMessage);
        } else {
          alert('회원가입 중 오류가 발생했습니다.');
        }
      });
  };

  // 로그인
  const login = function (payload) {
    axios({
      method: 'post',
      url: '/accounts/login/',
      data: {
        username: payload.username,
        password: payload.password,
      },
    })
      .then((res) => {
        token.value = res.data.key;
        localStorage.setItem('token', res.data.key);
        fetchUserInfo(); // 사용자 정보 가져오기
        router.push({ name: 'home' });
      })
      .catch((err) => {
        console.error(err);
        alert('로그인에 실패했습니다.');
      });
  };

  // 로그아웃
  const logout = function () {
    axios({
      method: 'post',
      url: '/accounts/logout/',
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then(() => {
        token.value = null;
        user.value = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        router.push({ name: 'login' });
      })
      .catch((err) => {
        console.error(err);
      });
  };

  const resetPassword = function(email) {
    // 이메일 중복 확인 후 비밀번호 초기화 진행
    axios({
      method: 'post',
      url: '/accounts/custom/check-email/',
      data: { email }
    })
      .then((res) => {
        if (!res.data.exists) {
          alert('등록되지 않은 이메일입니다.')
          return
        }
        // 비밀번호 초기화 요청
        axios({
          method: 'post',
          url: '/accounts/password/reset/',
          data: { email }
        })
          .then(() => {
            alert('비밀번호 재설정 이메일이 발송되었습니다.')
          })
      })
      .catch((err) => {
        console.error(err)
        alert('이메일 확인에 실패했습니다.')
      })
  }

  

  // 사용자 정보 조회
  const fetchUserInfo = function () {
    axios({
      method: 'get',
      url: '/accounts/user/',
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then((response) => {
        user.value = response.data;
        localStorage.setItem('user', JSON.stringify(response.data)); // 사용자 정보 저장
      })
      .catch((err) => {
        console.error(err);
        alert('사용자 정보를 불러오는데 실패했습니다.');
      });
  };

  // 사용자 정보 수정
  const updateUserInfo = function (userData) {
    axios({
      method: 'patch',
      url: '/accounts/user/',
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: userData,
    })
      .then((response) => {
        user.value = response.data;
        alert('프로필이 성공적으로 업데이트되었습니다.');
      })
      .catch((err) => {
        console.error(err);
        alert('프로필 업데이트에 실패했습니다.');
      });
  };

  // 토큰 및 사용자 정보 초기화
  const initializeToken = function () {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    if (storedToken) {
      token.value = storedToken;
    }
    if (storedUser) {
      user.value = JSON.parse(storedUser); // 저장된 user 정보 불러오기
    } else if (storedToken) {
      fetchUserInfo(); // user 정보가 없으면 서버에서 다시 가져오기
    }
  };

  return {
    token,
    user,
    isAuthenticated,
    register,
    login,
    logout,
    initializeToken,
    fetchUserInfo,
    updateUserInfo,
    resetPassword,
  };
}, {
  persist: {
    paths: ['token', 'user'],
  },
});
