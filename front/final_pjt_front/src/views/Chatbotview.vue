<template>
  <div class="container mt-4">
    <!-- 안내 모달 -->
    <div v-if="dialogue" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">안내</h5>
          </div>
          <div class="modal-body">
            <p>답변이 혹시 마음에 안드신다면</p>
            <p>답변에 마우스를 올리면 피드백을 하실 수 있습니다.</p>
            <p>감사합니다.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 채팅 토글 버튼 -->
    <div v-show="!hideflag" class="position-fixed bottom-0 end-0 m-3">
      <button class="btn btn-primary rounded-circle p-3" @click="hideflag = !hideflag">
        {{ button_title }}
      </button>
    </div>

    <!-- 채팅 창 -->
    <div v-show="hideflag" class="card shadow" style="max-width: 500px; margin: 0 auto;">
      <!-- 헤더 -->
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <button class="btn btn-outline-light btn-sm" @click="getmodal">?</button>
        <h5 class="mb-0">{{ title }}</h5>
        <div>
          <button class="btn btn-outline-light btn-sm me-2" @click="message_list=[]">
            <i class="bi bi-trash"></i>
          </button>
          <button class="btn btn-outline-light btn-sm" @click="hideflag = !hideflag">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
      </div>

      <!-- 채팅 내용 -->
      <div class="card-body chat-container" style="height: 400px; overflow-y: auto;">
        <div v-for="(message, idx) in message_list" :key="idx" class="mb-3">
          <!-- 사용자 메시지 -->
          <div v-if="message.type==='user'" class="d-flex justify-content-end">
            <div class="bg-primary text-white rounded p-2 max-w-75">
              {{ message.data }}
            </div>
          </div>
          <!-- 어시스턴트 메시지 -->
          <div v-else class="d-flex justify-content-start">
            <div class="bg-light rounded p-2 max-w-75 position-relative">
              <div v-if="message.loadflag" class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <span v-else>{{ message.data }}</span>
              <button v-if="!message.loadflag" 
                      class="btn btn-link position-absolute top-0 end-0 p-1"
                      @click="sendchat(message)">
                <i class="bi bi-exclamation-circle"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 입력창 -->
      <div class="card-footer">
        <div class="input-group">
          <input
            type="text"
            ref="chat"
            class="form-control"
            v-model="my_message"
            @keyup.enter="getChatData"
            placeholder="메시지를 입력하세요..."
          />
          <button class="btn btn-primary" @click="getChatData">
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

const dialogue = ref(false)
const hideflag = ref(true)
const title = ref('Seedly Assistant')
const button_title = ref('Chat')
const my_message = ref('')
const message_list = ref([])
const chat = ref(null)

const getmodal = () => {
  dialogue.value = true
  setTimeout(() => {
    dialogue.value = false
  }, 2000)
}

const sendchat = (message) => {
  console.log('피드백:', message)
}

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
</style>