import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import CustomSocketClient from '@/socket/customSocketClient'
import { useDroneStore } from './droneStore'
import { useTaskStore } from './taskStore'
import eventBus from './eventBus'

const SOCKET_STORAGE_KEY = 'socket_client_state'

function saveState(key, state) {
  localStorage.setItem(key, JSON.stringify(state))
}

function loadState(key, defaultValue) {
  const storedValue = localStorage.getItem(key)
  return storedValue && storedValue !== 'undefined' ? JSON.parse(storedValue) : defaultValue
}

export const useSocketStore = defineStore('socket', () => {
  const socketClient = ref(null)
  const drones = ref(loadState('socket_drones', []))
  const tasks = ref(loadState('socket_tasks', []))
  const assignedTasks = ref(loadState('socket_assigned_tasks', []))
  const executingTasks = ref(loadState('socket_executing_tasks', []))
  const roomId = ref(loadState('socket_roomId', ''))
  const droneStore = useDroneStore()
  const taskStore = useTaskStore()
  const isConnected = ref(loadState('socket_isConnected', false))
  const storedSocketState = loadState(SOCKET_STORAGE_KEY, null)

  function initialize(userId) {
    if (socketClient.value) {
      console.log('Already Initialized')
      socketClient.value.connect()
    } else if (storedSocketState && storedSocketState.url) {
      console.log('Socket State Initialized')
      socketClient.value = CustomSocketClient.getInstance(storedSocketState.url, roomId.value)
    } else {
      console.log('New Socket Initialized')
      socketClient.value = CustomSocketClient.getInstance('ws://127.0.0.1:8888/websocket', userId)
    }
    roomId.value = userId

    socketClient.value.on('connect', () => {
      console.log('Connected')
      isConnected.value = true
    })

    socketClient.value.on('disconnect', () => {
      console.log('Disconnected')
      isConnected.value = false
    })

    socketClient.value.on('filter_drones', () => {
      filterDrones()
    })

    socketClient.value.on('filter_tasks', () => {
      filterTasks()
    })

    socketClient.value.on('drone_data', (data) => {
      eventBus.drones = data
      drones.value = data
    })

    socketClient.value.on('task_data', (data) => {
      eventBus.tasks = data
      tasks.value = data
    })

    socketClient.value.on('assigned_task_data', (data) => {
      eventBus.assignedTasks = data
      assignedTasks.value = data
    })

    socketClient.value.on('executing_task_data', (data) => {
      eventBus.executingTasks = data
      executingTasks.value = data
    })

    socketClient.value.on('join_room', () => {
      console.log('Room Joined')
      joinRoom(userId)
    })
  }

  function updateDroneStatus(droneId, userId) {
    socketClient.value.emit('update_connection_status', { id: droneId, user_id: userId })
  }

  function filterDrones() {
    socketClient.value.emit('filter_drones', droneStore.filterDronesSocket())
  }

  function filterTasks() {
    socketClient.value.emit('filter_tasks', taskStore.filterTasksSocket())
  }

  function filterAssignedTasks(selectedDroneId) {
    socketClient.value.emit(
      'filter_assigned_tasks',
      taskStore.filterAssignedTasksSocket(selectedDroneId)
    )
  }

  function filterExecutingTasks(selectedDroneId) {
    socketClient.value.emit(
      'filter_executing_tasks',
      taskStore.filterExecutingTasksSocket(selectedDroneId)
    )
  }

  function joinRoom(userId) {
    socketClient.value.emit('join_room', { room: userId })
  }

  function disconnect(userId) {
    socketClient.value.emit('leave_room', { room: userId })
    socketClient.value.disconnect()
  }

  watch(
    drones,
    (newValue) => {
      saveState('socket_drones', newValue)
      eventBus.drones = newValue
    },
    { deep: true }
  )

  watch(
    tasks,
    (newValue) => {
      saveState('socket_tasks', newValue)
      eventBus.tasks = newValue
    },
    { deep: true }
  )

  watch(
    assignedTasks,
    (newValue) => {
      saveState('socket_assigned_tasks', newValue)
      eventBus.assignedTasks = newValue
    },
    { deep: true }
  )

  watch(
    executingTasks,
    (newValue) => {
      saveState('socket_executing_tasks', newValue)
      eventBus.executingTasks = newValue
    },
    { deep: true }
  )

  watch(isConnected, (newValue) => saveState('socket_isConnected', newValue))

  watch(roomId, (newValue) => saveState('socket_roomId', newValue))

  watch(
    socketClient,
    (newValue) => {
      if (newValue) {
        saveState(SOCKET_STORAGE_KEY, { url: newValue.url })
      }
    },
    { deep: true }
  )

  return {
    socketClient,
    drones,
    tasks,
    initialize,
    updateDroneStatus,
    filterDrones,
    filterTasks,
    filterAssignedTasks,
    filterExecutingTasks,
    disconnect,
    joinRoom
  }
})
