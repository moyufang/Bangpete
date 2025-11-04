<template>
  <div class="lobby">
    <h1>图片查看器</h1>
    
    <div class="controls">
      <button @click="prevImage" :disabled="loading">-1</button>
      <span class="song-id">当前 ID: {{ songId }}</span>
      <button @click="nextImage" :disabled="loading">+1</button>
    </div>
    
    <SongCard :song_id="songId"/>

    <div v-if="is_error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useLobbyStore } from '@/stores/lobby'
import { CARD_DEFAULT_JACKET_URL } from '@/config'

import SongCard from '@/components/SongCard.vue'

const lobbyStore = useLobbyStore()
const songId = ref<number>(306) // 初始 ID
const loading = ref(false)
const is_error = ref(false)
const error = ref('')

// 计算当前图片的文件路径
const currentImagePath = computed(() => `jacket/j-${songId.value}.png`)

// 计算当前图片的 URL
const currentImageUrl = computed(() => {
  const cachedUrl = lobbyStore.getImageUrl(currentImagePath.value)
  return cachedUrl || CARD_DEFAULT_JACKET_URL
})

// 图片加载失败处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = CARD_DEFAULT_JACKET_URL
  error.value = `图片 j-${songId.value}.png 加载失败`
}

// 加载当前图片
const loadCurrentImage = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await lobbyStore.fetchImageResource(currentImagePath.value)
    is_error.value = false
  } catch (err) {
    is_error.value = true
    error.value = `无法加载图片 j-${songId.value}.png`
    console.error('加载失败:', err)
  } finally {
    loading.value = false
  }
}

// 下一张图片
const nextImage = () => {
  songId.value += 1
}

// 上一张图片
const prevImage = () => {
  if (songId.value > 1) {
    songId.value -= 1
  }
}

// 监听 songId 变化，自动加载新图片
watch(songId, () => {
  loadCurrentImage()
})

// 初始化加载
onMounted(() => {
  loadCurrentImage()
})
</script>

<style scoped lang="scss">
.lobby {
  // max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;

  @include flex(column, flex-start, center)
}

.controls {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.controls button {
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
}

.controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.song-id {
  font-size: 18px;
  font-weight: bold;
  min-width: 120px;
}

</style>