<template>
  <div class="text-input-container">
    <label :for="inputId" class="text-input-label">{{ label }}</label>
    <input
      :id="inputId"
      type="text"
      :placeholder="placeholder"
      v-model="inputValue"
      class="text-input"
    />
  </div>
</template>

<style scoped>
.text-input-container {
  display: flex;
  flex-direction: column;
  margin: 20px 0;
}

.text-input-label {
  margin-bottom: 8px;
  font-size: 14px;
  color: #fff;
  font-family: 'Montserrat', sans-serif;
}

.text-input {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  font-size: 16px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  transition:
    border-color 0.3s,
    background-color 0.3s;
}

.text-input:focus {
  outline: none;
  border-color: #888;
  background-color: #fff;
}

.text-input::placeholder {
  color: #aaa;
}
</style>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  label: {
    type: String,
    default: 'Enter text'
  },
  placeholder: {
    type: String,
    default: 'Type something...'
  },
  modelValue: {
    type: String,
    default: ''
  },
  inputId: {
    type: String,
    default: 'textInput'
  }
})

const inputValue = ref(props.modelValue)

// Emit event
const emit = defineEmits(['update:modelValue'])

// Watch for changes in inputValue and emit the update
watch(inputValue, (newValue) => {
  emit('update:modelValue', newValue)
})
</script>
