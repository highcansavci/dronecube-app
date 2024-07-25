import { reactive, watch } from 'vue'

// Key used for local storage
const EVENT_BUS_STORAGE_KEY = 'event_bus_state'

// Function to save the state to local storage
function saveState(key, state) {
  localStorage.setItem(key, JSON.stringify(state))
}

// Function to load the state from local storage
function loadState(key, defaultValue) {
  const storedValue = localStorage.getItem(key)
  return storedValue && storedValue !== 'undefined' ? JSON.parse(storedValue) : defaultValue
}

// Initialize eventBus with reactive state
const eventBus = reactive(loadState(EVENT_BUS_STORAGE_KEY, {}))

// Watch the eventBus and save state to local storage on changes
watch(
  eventBus,
  (newState) => {
    saveState(EVENT_BUS_STORAGE_KEY, newState)
  },
  { deep: true }
)

export default eventBus
