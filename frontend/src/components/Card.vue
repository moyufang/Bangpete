<template>
  <div class="card">
    <div class="jacket">
      <img
        :src="imageUrl"
        :alt="song_header.jacket_name"
      />
    </div>
    
    <Diff :diff="song_header.diff"/>

    <h3 class="song_title">
      {{ song_header.title }}
    </h3>
    <h4 class="band_title">
      {{ song_header.band_id }}
    </h4>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'
import { SongHeader } from '@/types/SongHeader'
import Diff from './Diff.vue';
import get from '@/api/get';
import * as config from '@/config';

// 定义组件 Props
const props = defineProps<{
  song_header: SongHeader
}>()

// 图片缓存
const imageCache = new Map<string, string>()

// 响应式图片URL
const imageUrl = ref(config.CARD_DEFAULT_JACKET_URL)

// 当前加载的图片ID，用于防止竞态条件
let currentLoadId = 0

// 加载图片函数
const loadImage = async (songHeader: SongHeader) => {
  const loadId = ++currentLoadId
  const fileName = `j-${songHeader.song_id}.png`
  
  // 检查缓存
  if (imageCache.has(fileName)) {
    if (loadId === currentLoadId) {
      imageUrl.value = imageCache.get(fileName)!
    }
    return
  }
  
  try {
    const jacketBlob = await get.getJacketFile(fileName)
    if (loadId === currentLoadId) {
      const url = URL.createObjectURL(jacketBlob)
      imageUrl.value = url
      imageCache.set(fileName, url) // 缓存URL
    }
  } catch (error) {
    if (loadId === currentLoadId) {
      console.warn(`图片加载失败: ${fileName}`)
      imageUrl.value = config.CARD_DEFAULT_JACKET_URL
    }
  }
}

// 监听 song_header 变化
watch(() => props.song_header, (newHeader) => {
  loadImage(newHeader)
}, { immediate: true })

// 组件卸载时清理 ObjectURL
onUnmounted(() => {
  // 清理当前组件的 ObjectURL
  if (imageUrl.value && imageUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(imageUrl.value)
  }
  
  // 注意：这里不清理缓存，因为缓存是全局的，其他组件可能还在使用
  // 如果需要在应用级别清理缓存，可以在应用退出时统一清理
})
</script>

<style scoped lang="scss">
.card{
  background: none;
  width:  fit-content;
  height: fit-content;
  
  border: 0px;
  padding: 0px;

  @include flex(column, start, center);
  gap: $spacing-sm;

  transition: transform 0.3s ease;
  .card:hover {
    // transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }
}

.card .jacket{
  background: none;
  width: $jacket-size;
  height: $jacket-size;
  margin:0px;
  border:0px;
  border-radius: $border-radius-2xl;
  padding: 0px;
}

.card .song_title{
  color: $song-title-color
}

.card .band_title{
  color: $band-title-color;
}

</style>