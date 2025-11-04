<template>
  <div class="card">
    <div class="jacket">
      <img
        :src="img_url"
        :alt="song_header.jacket_name"
        @error="hander_img_error"
      />
    </div>
    
    <Diff :diff="song_diff"/>

    <h3 class="song_title">
      {{ song_header.title }}
    </h3>
    <h4 class="band_title">
      {{ song_author }}
    </h4>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { SongHeader, DEAULT_SONG_HEADER} from '@/types/SongHeader'
import Diff from './Diff.vue';
import * as cfg from '@/config';
import { useLobbyStore } from '@/stores/lobby';
const lobbyStore = useLobbyStore();

// 定义组件 Props
const props = defineProps<{
  song_id: number
}>()


const song_authors = ref<Record<string, any>>({});
const songs_header = ref<Record<number, SongHeader>>({});

const song_header = computed(():SongHeader=> props.song_id in songs_header.value ? songs_header.value[props.song_id] : DEAULT_SONG_HEADER)
const song_author = computed(():string=> song_header.value.band_id !== -1 ? song_authors.value[`${song_header.value.band_id}`]["bang_name"] : "nop")
const song_diff   = computed(():number[]=> song_header.value.diff)
const jacket_url = computed(() => `jacket/j-${props.song_id}.png`)
const img_url = computed(()=>{
  return lobbyStore.getImageUrl(jacket_url.value) || cfg.CARD_DEFAULT_JACKET_URL
}) 

const loading = ref(false)
const is_error = ref(false)
const error = ref('')

const fetch_img = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await lobbyStore.fetchImageResource(jacket_url.value)
    is_error.value = false
  } catch (err) {
    is_error.value = true
    error.value = `无法加载图片 j-${props.song_id}.png`
    console.error('加载失败:', err)
  } finally {
    loading.value = false
  }
}

const hander_img_error = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = cfg.CARD_DEFAULT_JACKET_URL
  error.value = `图片 j-${props.song_id}.png 加载失败`
}

// 监听 song_header 变化
watch(() => props.song_id, () => {
  fetch_img();
  console.log(song_diff.value)
}, { immediate: true })

onMounted(async()=>{
  await Promise.all([
    lobbyStore.fetchJsonResource(cfg.SONG_AUTHORS_URL),
    lobbyStore.fetchJsonResource(cfg.SONGS_HEADER_URL)
  ]);

  song_authors.value = lobbyStore.getJsonData(cfg.SONG_AUTHORS_URL);
  songs_header.value = lobbyStore.getJsonData(cfg.SONGS_HEADER_URL);

  await fetch_img();
})

</script>

<style scoped lang="scss">
.card{
  background-color: black;
  width:  fit-content;
  height: fit-content;
  
  border: 0px;
  border-radius: 0px;
  padding: 0px;

  @include flex(column, start, center);
  gap: $spacing-sm;

  // transition: transform 0.3s ease;
  // .card:hover {
  //   // transform: translateY(-4px);
  //   box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  // }
  & .jacket{
    width: $jacket-size;
    height: $jacket-size;
    margin:0px;
    border:0px;
    border-radius: $border-radius-2xl;
    padding: 0px;
  }

  & .song_title{
    color: $song-title-color
  }

  & .band_title{
    color: $band-title-color;
  }
}

</style>