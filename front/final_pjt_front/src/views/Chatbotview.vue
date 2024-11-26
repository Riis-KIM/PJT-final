<template>
  <div class="container mt-4">
    <!-- 채팅 창 -->
    <div class="card shadow-sm cute-card">
      <!-- 헤더 -->
      <div class="card-header bg-green text-white d-flex justify-content-between align-items-center cute-header">
        <h5 class="mb-0">{{ title }}</h5>
        <button class="btn btn-outline-light btn-sm" @click="message_list = []">
          <i class="bi bi-trash"></i>
        </button>
      </div>

      <!-- 채팅 내용 -->
      <div class="card-body chat-container bg-light" style="height: 500px; overflow-y: auto;">
        <div v-for="(message, idx) in message_list" :key="idx" class="mb-3">
          <!-- 사용자 메시지 -->
          <div v-if="message.type === 'user'" class="d-flex justify-content-end">
            <div class="user-message cute-user-message rounded p-2 max-w-75">
              {{ message.data }}
            </div>
          </div>
          <!-- 어시스턴트 메시지 -->
          <div v-else class="d-flex justify-content-start">
            <div class="assistant-message cute-assistant-message rounded p-3 max-w-75 position-relative shadow-sm">
              <div v-if="message.loadflag" class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <div v-else v-html="sanitizeHtml(message.data)"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 입력창 -->
      <div class="card-footer bg-light border-top">
        <div class="input-group">
          <input
            type="text"
            ref="chat"
            class="form-control border-green cute-input"
            v-model="my_message"
            @keyup.enter="getChatData"
            placeholder="메시지를 입력하세요..."
          />
          <button class="btn btn-green cute-button" @click="getChatData">전송</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// Title and reactive variables
const title = ref("Seedly Assistant");
const my_message = ref("");
const message_list = ref([]);
const chat = ref(null);

// Function to send and retrieve chat data
const getChatData = async () => {
  if (!my_message.value) return;

  message_list.value.push({
    type: "user",
    data: my_message.value,
  });

  message_list.value.push({
    type: "assistant",
    data: "",
    loadflag: true,
  });

  try {
    const response = await axios.post("/chat/message/", {
      message: my_message.value,
    });

    message_list.value[message_list.value.length - 1] = {
      type: "assistant",
      data: response.data.message,
      loadflag: false,
    };
  } catch (error) {
    console.error("API 오류:", error);
    message_list.value[message_list.value.length - 1] = {
      type: "assistant",
      data: "죄송합니다. 오류가 발생했습니다.",
      loadflag: false,
    };
  }

  my_message.value = "";
};

// Sanitize HTML or Markdown syntax
const sanitizeHtml = (content) => {
  // Replace '**' or other Markdown syntax with HTML equivalent
  return content
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Bold
    .replace(/__(.*?)__/g, "<em>$1</em>"); // Italics
};

onMounted(() => {
  if (chat.value) {
    chat.value.focus();
  }
});
</script>

<style scoped>
/* 전체 카드 스타일 */
.cute-card {
  border-radius: 15px;
  background: #edf7ed; /* 연한 초록색 배경 */
}

/* 헤더 스타일 */
.cute-header {
  background: #28a745; /* 메인 초록색 */
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  font-weight: bold;
}

/* 사용자 메시지 스타일 */
.cute-user-message {
  background: #d4edda; /* 사용자 메시지 연한 초록색 */
  color: #333;
  border-radius: 20px;
  font-size: 0.9rem;
  padding: 0.8rem;
}

/* 어시스턴트 메시지 스타일 */
.cute-assistant-message {
  background: #ffffff;
  color: #333;
  border: 1px solid #28a745;
  border-radius: 20px;
  font-size: 0.9rem;
  padding: 0.8rem;
}

/* 입력창 스타일 */
.cute-input {
  border: 2px solid #28a745; /* 메인 초록색 */
  border-radius: 20px;
  font-size: 1rem;
  padding: 0.5rem;
}

.cute-input:focus {
  outline: none;
  border-color: #81c784; /* 포커스 초록색 */
}

/* 버튼 스타일 */
.cute-button {
  background: #28a745; /* 메인 초록색 */
  color: white;
  font-size: 0.9rem;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  transition: background 0.3s ease;
}

.cute-button:hover {
  background: #81c784; /* 버튼 호버 연한 초록색 */
  color: white;
}

/* 스크롤바 커스터마이징 */
.chat-container {
  overflow-y: auto;
}

.chat-container::-webkit-scrollbar {
  width: 8px;
}

.chat-container::-webkit-scrollbar-thumb {
  background-color: #81c784; /* 초록색 스크롤바 */
  border-radius: 5px;
}

.chat-container::-webkit-scrollbar-track {
  background: #edf7ed; /* 연한 초록 배경 */
}
</style>
