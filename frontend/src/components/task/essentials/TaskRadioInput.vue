<template>
  <label class="sidebar-label-container">
    <input
      type="radio"
      :value="value"
      :name="name"
      :checked="modelValue === value"
      @change="handleChange"
    />
    <span class="checkmark"></span>{{ title }}
  </label>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// Define props
// eslint-disable-next-line no-unused-vars
const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean],
    required: true
  },
  value: {
    type: [String, Number, Boolean],
    required: true
  },
  name: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
})

// Emitting updates to parent component
const emit = defineEmits(['update:modelValue'])

// Handle change event of the radio input
const handleChange = (event) => {
  emit('update:modelValue', event.target.value)
}
</script>

<style scoped>
.sidebar-label-container {
  display: block;
  position: relative;
  color: #fff;
  padding-left: 35px;
  margin-bottom: 12px;
  cursor: pointer;
  user-select: none;
}

.sidebar-label-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 20px;
  width: 20px;
  background-color: #eee;
  border-radius: 50%;
}

.sidebar-label-container:hover input ~ .checkmark {
  background-color: #ccc;
}

.sidebar-label-container input:checked ~ .checkmark {
  background-color: #2196f3;
}

.checkmark::after {
  content: '';
  position: absolute;
  display: none;
}

.sidebar-label-container input:checked ~ .checkmark::after {
  display: block;
}

.sidebar-label-container .checkmark::after {
  top: 6.4px;
  left: 6.4px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: white;
}
</style>
