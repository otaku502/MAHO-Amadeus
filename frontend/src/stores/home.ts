import { defineStore } from 'pinia'
import { ref } from 'vue'
import config from '../config.json'
import { MahoWebSocket } from '../api/ws'

export const useHomeStore = defineStore('home', () => {
  // 文本框相关
  const textQueue = ref<string[]>([])
  const thinkText = ref('')
  // 音频相关
  const audioQueue = ref<{ data: string, is_final: boolean }[]>([])
  const mouthOpen = ref(0) // 嘴巴张开程度 0-1
  
  // 按钮状态
  const buttonStates = ref({
    video: false
  })
  
  // 用户名
  const userName = ref(localStorage.getItem('username') || '未命名')
  const amadeusName = ref(config.amadeusName || '比屋定真帆')
  const currentName = ref(userName.value)


  // WS客户端
  const wsClient = new MahoWebSocket()

  // WS状态
  const isWaiting = ref(false)
  const wsStatus = ref('closed')

  // 注册 WebSocket 回调函数
  wsClient.on('open', () => {
    wsStatus.value = 'connected'
  })

  wsClient.on('close', () => {
    wsStatus.value = 'closed'
  })

  wsClient.on('thinkText', (msg: any) => {
    thinkText.value += msg.data
  })

  wsClient.on('text', (msg: any) => {
    if (thinkText.value) {
      thinkText.value = ''
    }
    textQueue.value.push(msg.data)
  })

  wsClient.on('audio', (msg: any) => {
    audioQueue.value.push({
      data: msg.data,
      is_final: msg.is_final
    })
  })

  wsClient.on('start', () => {
    textQueue.value = []
    thinkText.value = ''
    isWaiting.value = true
    currentName.value = amadeusName.value
  })

  wsClient.on('end', () => {
    currentName.value = userName.value
    isWaiting.value = false
  })

  function send(data: any) {
    wsClient.send(data)
  }

  return {
    textQueue,
    thinkText,
    audioQueue,
    isWaiting,
    wsStatus,
    buttonStates,
    mouthOpen,
    currentName,
    send
  }
})