<template>
  <div>
    <h1>커뮤니티</h1>
    <p>여러 금융 상품의 금리를 비교하세요.</p>

    <!-- 글 작성 버튼 (로그인한 사용자만 표시) -->
    <button
      v-if="isLoggedIn"
      @click="showWriteForm = !showWriteForm"
      class="btn btn-primary"
    >
      글 작성하기
    </button>
    <p v-else>로그인한 사용자만 글을 작성할 수 있습니다.</p>

    <!-- 글 작성 폼 -->
    <div v-if="showWriteForm" class="write-form">
      <textarea
        v-model="newPost.content"
        class="form-control mb-2"
        placeholder="글 내용을 입력하세요"
      ></textarea>
      <button @click="addPost" class="btn btn-success">작성</button>
      <button @click="showWriteForm = false" class="btn btn-secondary">
        취소
      </button>
    </div>

    <!-- 게시글 목록 -->
    <div v-for="post in posts" :key="post.id" class="post">
      <div class="post-header">
        <h3>{{ post.author }}</h3>
        <p>{{ post.content }}</p>

        <!-- 작성자만 수정/삭제 버튼 표시 -->
        <div v-if="post.author === currentUser">
          <button @click="editPost(post)" class="btn btn-warning btn-sm">
            수정
          </button>
          <button @click="deletePost(post.id)" class="btn btn-danger btn-sm">
            삭제
          </button>
        </div>
      </div>

      <!-- 댓글 작성 -->
      <div class="comment-section">
        <textarea
          v-if="isLoggedIn"
          v-model="newComment"
          class="form-control mb-2"
          placeholder="댓글을 입력하세요"
        ></textarea>
        <button v-if="isLoggedIn" @click="addComment(post)" class="btn btn-info">
          댓글 작성
        </button>
        <p v-else>로그인한 사용자만 댓글을 작성할 수 있습니다.</p>

        <!-- 댓글 목록 -->
        <div v-for="comment in post.comments" :key="comment.id" class="comment">
          <p>
            {{ comment.author }}: {{ comment.content }}
          </p>
          <div v-if="comment.author === currentUser">
            <button
              @click="editComment(post, comment)"
              class="btn btn-warning btn-sm"
            >
              수정
            </button>
            <button
              @click="deleteComment(post, comment.id)"
              class="btn btn-danger btn-sm"
            >
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CommunityView",
  data() {
    return {
      isLoggedIn: localStorage.getItem("isLoggedIn") === "true", // 로그인 상태
      currentUser: localStorage.getItem("currentUser") || "guest", // 현재 로그인한 사용자
      showWriteForm: false, // 글 작성 폼 표시 여부
      newPost: {
        id: null,
        content: "",
        author: "",
        comments: [],
      },
      posts: [], // 게시글 목록
      newComment: "", // 새로운 댓글 내용
    };
  },
  methods: {
    // 글 작성
    addPost() {
      if (this.newPost.content.trim() === "") {
        alert("글 내용을 입력하세요.");
        return;
      }
      const newPost = {
        id: Date.now(),
        content: this.newPost.content,
        author: this.currentUser,
        comments: [],
      };
      this.posts.push(newPost);
      this.newPost.content = "";
      this.showWriteForm = false;
    },

    // 글 수정
    editPost(post) {
      const newContent = prompt("수정할 내용을 입력하세요:", post.content);
      if (newContent !== null) {
        post.content = newContent;
      }
    },

    // 글 삭제
    deletePost(postId) {
      this.posts = this.posts.filter((post) => post.id !== postId);
    },

    // 댓글 작성
    addComment(post) {
      if (this.newComment.trim() === "") {
        alert("댓글 내용을 입력하세요.");
        return;
      }
      const newComment = {
        id: Date.now(),
        content: this.newComment,
        author: this.currentUser,
      };
      post.comments.push(newComment);
      this.newComment = "";
    },

    // 댓글 수정
    editComment(post, comment) {
      const newContent = prompt("수정할 댓글 내용을 입력하세요:", comment.content);
      if (newContent !== null) {
        comment.content = newContent;
      }
    },

    // 댓글 삭제
    deleteComment(post, commentId) {
      post.comments = post.comments.filter((comment) => comment.id !== commentId);
    },
  },
};
</script>

<style scoped>
div {
  text-align: center;
  padding: 20px;
}
.post {
  border: 1px solid #ddd;
  padding: 15px;
  margin: 15px 0;
  border-radius: 8px;
}
.comment-section {
  margin-top: 10px;
  text-align: left;
}
.comment {
  margin: 5px 0;
  padding-left: 15px;
  border-left: 2px solid #ddd;
}
</style>
