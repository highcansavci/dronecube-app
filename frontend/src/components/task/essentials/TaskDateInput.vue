<template>
  <div class="date-input-container">
    <div class="input-wrapper">
      <label :for="inputIdMin" class="date-input-label">Minimum Date</label>
      <input
        :id="inputIdMin"
        type="datetime-local"
        :min="min"
        :max="max"
        :placeholder="minPlaceholder"
        v-model="inputMinValue"
        @input="validateMinValue"
        class="date-input"
      />
    </div>
    <div class="input-wrapper">
      <label :for="inputIdMax" class="date-input-label">Maximum Date</label>
      <input
        :id="inputIdMax"
        type="datetime-local"
        :min="min"
        :max="max"
        :placeholder="maxPlaceholder"
        v-model="inputMaxValue"
        @input="validateMaxValue"
        class="date-input"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  minPlaceholder: {
    type: String,
    default: 'Min date...'
  },
  maxPlaceholder: {
    type: String,
    default: 'Max date...'
  },
  minValue: {
    type: Date,
    default: () => new Date(1900, 0, 1)
  },
  maxValue: {
    type: Date,
    default: () => new Date(2100, 11, 31)
  },
  inputIdMin: {
    type: String,
    default: 'dateInputMin'
  },
  inputIdMax: {
    type: String,
    default: 'dateInputMax'
  },
  min: {
    type: Date,
    default: () => new Date(1900, 0, 1)
  },
  max: {
    type: Date,
    default: () => new Date(2100, 11, 31)
  }
})

// Convert Date object to a datetime-local string
const toDateTimeLocal = (date) => {
  console.log(date)
  if (date === null) {
    return
  }
  const pad = (num) => String(num).padStart(2, '0')
  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1)
  const day = pad(date.getDate())
  const hours = pad(date.getHours())
  const minutes = pad(date.getMinutes())
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

// Reactive references for input values
const inputMinValue = ref(toDateTimeLocal(props.minValue))
const inputMaxValue = ref(toDateTimeLocal(props.maxValue))

// Emit event
const emit = defineEmits(['update:minValue', 'update:maxValue'])

// Watch for changes in inputMinValue and inputMaxValue and emit the updates
watch(inputMinValue, (newValue) => {
  const newDate = new Date(newValue)
  if (newDate < props.min) {
    inputMinValue.value = toDateTimeLocal(props.min)
  } else if (newDate > new Date(inputMaxValue.value)) {
    inputMaxValue.value = toDateTimeLocal(newDate)
  }
  emit('update:minValue', newDate)
})

watch(inputMaxValue, (newValue) => {
  const newDate = new Date(newValue)
  if (newDate > props.max) {
    inputMaxValue.value = toDateTimeLocal(props.max)
  } else if (newDate < new Date(inputMinValue.value)) {
    inputMinValue.value = toDateTimeLocal(newDate)
  }
  emit('update:maxValue', newDate)
})

// Validate inputMinValue and ensure it doesn't exceed max
const validateMinValue = () => {
  const newDate = new Date(inputMinValue.value)
  if (newDate < props.min) {
    inputMinValue.value = toDateTimeLocal(props.min)
  } else if (newDate > new Date(inputMaxValue.value)) {
    inputMinValue.value = inputMaxValue.value
  }
}

// Validate inputMaxValue and ensure it doesn't go below min
const validateMaxValue = () => {
  const newDate = new Date(inputMaxValue.value)
  if (newDate > props.max) {
    inputMaxValue.value = toDateTimeLocal(props.max)
  } else if (newDate < new Date(inputMinValue.value)) {
    inputMaxValue.value = inputMinValue.value
  }
}
</script>

<style scoped>
.date-input-container {
  display: flex;
  flex-direction: column;
  row-gap: 6px;
  margin: 20px 0;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
}

.date-input-label {
  margin-bottom: 8px;
  font-size: 14px;
  color: #fff;
  font-family: 'Montserrat', sans-serif;
}

.date-input {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  font-size: 16px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  width: 95%;
  transition:
    border-color 0.3s,
    background-color 0.3s;
}

.date-input:focus {
  outline: none;
  border-color: #888;
  background-color: #fff;
}

.date-input::placeholder {
  color: #aaa;
}

@media (max-width: 768px) {
  .date-input-container {
    flex-direction: column;
  }
  .input-wrapper {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .date-input-container {
    margin: 10px 0;
  }
  .date-input {
    padding: 8px;
    font-size: 14px;
  }
}

@media (max-width: 320px) {
  .date-input-label {
    font-size: 12px;
  }
  .date-input {
    padding: 6px;
    font-size: 12px;
  }
}
</style>
