<template>
  <div class="pagination">
    <button @click="gotoPage(1)" :disabled="currentPage === 1">First</button>
    <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
    <span>Page {{ currentPage }} of {{ totalPages }}</span>
    <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    <button @click="gotoPage(totalPages)" :disabled="currentPage === totalPages">
      Last
    </button>
  </div>
</template>

<script setup>
import { defineProps, ref, watch, getCurrentInstance } from "vue";

const props = defineProps({
  totalPages: {
    type: Number,
    required: true,
  },
  currentPage: {
    type: Number,
    required: true,
  },
});

const currentPage = ref(props.currentPage);
const { emit } = getCurrentInstance();

const nextPage = () => {
  if (currentPage.value < props.totalPages) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const gotoPage = (page) => {
  currentPage.value = page;
};

watch(currentPage, (newValue) => {
  emit("pageChange", newValue);
});
</script>

<style scoped>
.pagination {
  position: relative;
  height: 60px;
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 5px 5px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(3px);
  border-radius: 2px;
}

.pagination button,
.pagination span {
  position: relative;
  padding: 20px 25px;
  text-decoration: none;
  color: #fff;
  font-weight: 500;
}

.pagination button:hover,
.pagination button {
  background: rgba(255, 255, 255, 0.2);
}
</style>
