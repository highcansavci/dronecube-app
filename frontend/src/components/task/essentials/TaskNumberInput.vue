<template>
  <div class="number-input-container">
    <div class="input-wrapper">
      <label :for="inputIdMin" class="number-input-label">Minimum</label>
      <input
        :id="inputIdMin"
        type="number"
        step="0.00000000001"
        :min="min"
        :max="max"
        :placeholder="minPlaceholder"
        v-model.number="inputMinValue"
        @input="validateMinValue"
        class="number-input"
      />
    </div>
    <div class="input-wrapper">
      <label :for="inputIdMax" class="number-input-label">Maximum</label>
      <input
        :id="inputIdMax"
        type="number"
        step="0.00000000001"
        :min="min"
        :max="max"
        :placeholder="maxPlaceholder"
        v-model.number="inputMaxValue"
        @input="validateMaxValue"
        class="number-input"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  label: {
    type: String,
    default: 'Enter value'
  },
  minPlaceholder: {
    type: String,
    default: 'Min value...'
  },
  maxPlaceholder: {
    type: String,
    default: 'Max value...'
  },
  minValue: {
    type: Number,
    default: 0
  },
  maxValue: {
    type: Number,
    default: 100
  },
  inputIdMin: {
    type: String,
    default: 'textInputMin'
  },
  inputIdMax: {
    type: String,
    default: 'textInputMax'
  },
  min: {
    type: Number,
    default: -Infinity
  },
  max: {
    type: Number,
    default: Infinity
  }
})

// Utility function to convert value to number
const convertToNumber = (value, defaultValue) => {
  const number = Number(value)
  return isNaN(number) ? defaultValue : number
}

// Reactive references for input values
const inputMinValue = ref(convertToNumber(props.minValue, props.min))
const inputMaxValue = ref(convertToNumber(props.maxValue, props.max))

// Emit event
const emit = defineEmits(['update:minValue', 'update:maxValue'])

// Watch for changes in inputMinValue and inputMaxValue and emit the updates
watch(inputMinValue, (newValue, oldValue) => {
  if (newValue === '') {
    inputMinValue.value = props.min
  } else {
    const value = convertToNumber(newValue, oldValue)
    if (value < props.min) {
      inputMinValue.value = props.min
    } else if (value > inputMaxValue.value) {
      inputMaxValue.value = value
    }
  }
  emit('update:minValue', inputMinValue.value)
})

watch(inputMaxValue, (newValue, oldValue) => {
  if (newValue === '') {
    inputMaxValue.value = props.max
  } else {
    const value = convertToNumber(newValue, oldValue)
    if (value > props.max) {
      inputMaxValue.value = props.max
    } else if (value < inputMinValue.value) {
      inputMinValue.value = value
    }
  }
  emit('update:maxValue', inputMaxValue.value)
})

// Validate inputMinValue and ensure it doesn't exceed max
const validateMinValue = () => {
  if (inputMinValue.value === '') {
    inputMinValue.value = props.min
  } else if (inputMinValue.value < props.min) {
    inputMinValue.value = props.min
  } else if (inputMinValue.value > inputMaxValue.value) {
    inputMinValue.value = inputMaxValue.value
  }
}

// Validate inputMaxValue and ensure it doesn't go below min
const validateMaxValue = () => {
  if (inputMaxValue.value === '') {
    inputMaxValue.value = props.max
  } else if (inputMaxValue.value > props.max) {
    inputMaxValue.value = props.max
  } else if (inputMaxValue.value < inputMinValue.value) {
    inputMaxValue.value = inputMinValue.value
  }
}
</script>

<style scoped>
.number-input-container {
  display: flex;
  flex-direction: row;
  row-gap: 6px;
  margin: 20px 0;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
}

.number-input-label {
  margin-bottom: 8px;
  font-size: 14px;
  color: #fff;
  font-family: 'Montserrat', sans-serif;
}

.number-input {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  font-size: 16px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  width: 90%;
  transition:
    border-color 0.3s,
    background-color 0.3s;
}

.number-input:focus {
  outline: none;
  border-color: #888;
  background-color: #fff;
}

.number-input::placeholder {
  color: #aaa;
}

@media (max-width: 768px) {
  .number-input-container {
    flex-direction: column;
  }
  .input-wrapper {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .number-input-container {
    margin: 10px 0;
  }
  .number-input {
    padding: 8px;
    font-size: 14px;
  }
}

@media (max-width: 320px) {
  .number-input-label {
    font-size: 12px;
  }
  .number-input {
    padding: 6px;
    font-size: 12px;
  }
}
</style>
