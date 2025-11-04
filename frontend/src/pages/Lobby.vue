<script setup lang="ts">
import {onMounted, ref} from 'vue'
import Card from '@/components/Card.vue';
import api, {SongConstraint} from "@/api/get"
import axios from 'axios';

// 搜索歌曲


onMounted(async()=>{
  const result = await api.searchSong('233')
  console.log(result);

  // 获取歌曲列表
  const constraint: SongConstraint = {
    diff: 2,
    level_low: 20,
    level_high: 25,
    band_id: 1,
    start_count: 1,
    page_size: 10
  }
  const listResult = await api.getSongList(constraint)
   console.log(listResult);

  // 获取图片文件
  const fileName = 'j-513.png';
  try {
    const jacketBlob = await api.getJacketFile(fileName);
    console.log(jacketBlob);
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      console.warn(`图片文件不存在: ${fileName}`);
      return null; // 或者返回一个默认图片
    }
  }
  
})

</script>

<template>
  <div class="container">
    <!-- <Card :song_header=""/> -->
    <div>Fuckyou</div>
  </div>
</template>

<style scoped lang='scss'>

.container{
  background: none;
  width: 100vw;
  height: 100vh;

  @include purebox();
  @include flex('column', 'center', 'center');
}

</style>