class CustomSocketClient {
  constructor(url, roomId) {
    if (CustomSocketClient.instanceMap.has(roomId)) {
      return CustomSocketClient.instanceMap.get(roomId)
    }

    this.url = url
    this.socket = null
    this.roomId = roomId
    this.eventHandlers = {}

    CustomSocketClient.instanceMap.set(roomId, this)
    this.connect()
  }

  static getInstance(url, roomId) {
    if (!CustomSocketClient.instanceMap.has(roomId)) {
      new CustomSocketClient(url, roomId)
    }
    return CustomSocketClient.instanceMap.get(roomId)
  }

  connect() {
    if (this.socket) {
      this.emit('leave_room', { room: this.roomId })
      this.emit('disconnect')
      this.socket.close()
      this.socket = null
    }

    this.socket = new WebSocket(this.url)

    this.socket.onopen = () => {
      console.log('WebSocket connection established')
      this.emit('connect') // Trigger the connect event
    }

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data)
      console.log('Message from server:', message)
      this.handleEvent(message.event, message.data)
    }

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event)
    }
  }

  on(event, handler) {
    if (!this.eventHandlers[event]) {
      this.eventHandlers[event] = []
    }
    this.eventHandlers[event].push(handler)
  }

  emit(event, data) {
    const message = { event, data }
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message))
    } else {
      console.error('WebSocket is not connected.')
    }
  }

  handleEvent(event, data) {
    const handlers = this.eventHandlers[event]
    if (handlers) {
      handlers.forEach((handler) => handler(data))
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close()
      this.socket = null
    }
  }
}

CustomSocketClient.instanceMap = new Map()

export default CustomSocketClient
