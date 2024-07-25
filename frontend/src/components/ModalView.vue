<template>
  <div class="modal" v-if="isOpen">
    <div class="modal-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, watch } from 'vue'

const props = defineProps({
  isOpenProp: Boolean
})
const isOpen = ref(props.isOpenProp)

watch(
  () => props.isOpenProp,
  (newVal) => {
    isOpen.value = newVal
  }
)
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: linear-gradient(to right, #000000, gray);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: linear-gradient(to right, #000000, gray);
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  border-radius: 10px;
  position: relative;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
