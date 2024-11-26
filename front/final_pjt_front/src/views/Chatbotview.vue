<template>
  <div class="container mt-4">

    <!-- 채팅 창 -->
    <div class="card shadow-sm">
      <!-- 헤더 -->
      <div class="card-header bg-secondary text-white d-flex justify-content-between align-items-center">
        <p></p>
        <h5 class="mb-0">{{ title }}</h5>
        <button class="btn btn-outline-light btn-sm" @click="message_list=[]">
          <i class="bi bi-trash"></i>
        </button>
      </div>

      <!-- 채팅 내용 -->
      <div class="card-body chat-container bg-light" style="height: 500px; overflow-y: auto;">
        <div v-for="(message, idx) in message_list" :key="idx" class="mb-3">
          <!-- 사용자 메시지 -->
          <div v-if="message.type==='user'" class="d-flex justify-content-end">
            <div class="bg-secondary text-white rounded p-2 max-w-75">
              {{ message.data }}
            </div>
          </div>
          <!-- 어시스턴트 메시지 -->
          <div v-else class="d-flex justify-content-start">
            <div class="bg-white rounded p-2 max-w-75 position-relative shadow-sm">
              <div v-if="message.loadflag" class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <span v-else>{{ message.data }}</span>
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
            class="form-control border-secondary"
            v-model="my_message"
            @keyup.enter="getChatData"
            placeholder="메시지를 입력하세요..."
          />
          <button class="btn btn-secondary" @click="getChatData">
            전송
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const title = ref('Seedly Assistant')
const my_message = ref('')
const message_list = ref([])
const chat = ref(null)

const getChatData = async () => {
  if (!my_message.value) return

  message_list.value.push({
    type: 'user',
    data: my_message.value
  })

  message_list.value.push({
    type: 'assistant',
    data: '',
    loadflag: true
  })

  try {
    const response = await axios.post('/chat/message/', {
      message: my_message.value
    })

    message_list.value[message_list.value.length - 1] = {
      type: 'assistant',
      data: response.data.message,
      loadflag: false
    }
  } catch (error) {
    console.error('API 오류:', error)
    message_list.value[message_list.value.length - 1] = {
      type: 'assistant',
      data: '죄송합니다. 오류가 발생했습니다.',
      loadflag: false
    }
  }

  my_message.value = ''
}

onMounted(() => {
  if (chat.value) {
    chat.value.focus()
  }
})
</script>

<style scoped>
.max-w-75 {
  max-width: 75%;
}

.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.2);
  border-radius: 3px;
}

.modal {
  background-color: rgba(0,0,0,0.5);
}

.card {
  border-color: #dee2e6;
}

.bg-secondary {
  background-color: #6c757d !important;
}
</style>