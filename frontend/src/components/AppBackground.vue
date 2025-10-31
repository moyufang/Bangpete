<template>
  <div 
    class="app-background"
    :class="backgroundClasses"
    :style="backgroundStyles"
  >
    <!-- 背景图片层 -->
    <div 
      class="background-image"
      :style="imageStyles"
    ></div>
    
    <!-- 雾化效果层 -->
    <div 
      v-if="fogEffect"
      class="fog-layer"
      :style="fogStyles"
    ></div>
    
    <!-- 白化效果层 -->
    <div 
      v-if="whitenEffect"
      class="whiten-layer"
      :style="whitenStyles"
    ></div>
    
    <!-- 渐变叠加层 -->
    <div 
      v-if="gradientOverlay"
      class="gradient-overlay"
      :style="gradientStyles"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { computed, withDefaults } from 'vue'

// 组件属性定义
interface Props {
  // 背景图片路径
  imageUrl?: string
  // 雾化效果强度 (0-100)
  fogIntensity?: number
  // 雾化颜色
  fogColor?: string
  // 白化效果强度 (0-100)
  whitenIntensity?: number
  // 白化颜色
  whitenColor?: string
  // 渐变叠加
  gradientOverlay?: boolean
  // 渐变方向
  gradientDirection?: 'to top' | 'to bottom' | 'to left' | 'to right'
  // 渐变颜色
  gradientColors?: string[]
  // 模糊效果
  blur?: number
  // 亮度
  brightness?: number
  // 对比度
  contrast?: number
  // 饱和度
  saturation?: number
  // 是否固定背景（不随内容滚动）
  fixed?: boolean
  // 背景尺寸
  backgroundSize?: 'cover' | 'contain' | 'auto'
  // 背景位置
  backgroundPosition?: string
  // 是否启用视差效果
  parallax?: boolean
  // 视差强度
  parallaxIntensity?: number
}

// 默认属性值
const props = withDefaults(defineProps<Props>(), {
  imageUrl: '/src/assets/imgs/app_background.jpg',
  fogIntensity: 0,
  fogColor: 'rgba(255, 255, 255, 0.3)',
  whitenIntensity: 0,
  whitenColor: 'rgba(255, 255, 255, 0.5)',
  gradientOverlay: false,
  gradientDirection: 'to bottom',
  gradientColors: () => ['rgba(255,255,255,0)', 'rgba(255,255,255,0.8)'],
  blur: 0,
  brightness: 100,
  contrast: 100,
  saturation: 100,
  fixed: true,
  backgroundSize: 'cover',      //裁剪图片适应视窗大小
  backgroundPosition: 'center',
  parallax: false,
  parallaxIntensity: 0.5
})

// 计算属性
const fogEffect = computed(() => props.fogIntensity > 0)
const whitenEffect = computed(() => props.whitenIntensity > 0)

// 动态类名
const backgroundClasses = computed(() => ({
  'fixed-background': props.fixed,
  'parallax-background': props.parallax
}))

// 背景图片样式
const imageStyles = computed(() => {
  const styles: Record<string, string> = {
    backgroundImage: `url(${props.imageUrl})`,
    backgroundSize: props.backgroundSize,
    backgroundPosition: props.backgroundPosition,
    backgroundRepeat: 'no-repeat'
  }

  // 应用滤镜效果
  const filters = []
  if (props.blur > 0) filters.push(`blur(${props.blur}px)`)
  if (props.brightness !== 100) filters.push(`brightness(${props.brightness}%)`)
  if (props.contrast !== 100) filters.push(`contrast(${props.contrast}%)`)
  if (props.saturation !== 100) filters.push(`saturate(${props.saturation}%)`)

  if (filters.length > 0) {
    styles.filter = filters.join(' ')
  }

  return styles
})

// 雾化效果样式
const fogStyles = computed(() => {
  const intensity = Math.min(props.fogIntensity, 100) / 100
  return {
    backgroundColor: props.fogColor,
    opacity: intensity.toString()
  }
})

// 白化效果样式
const whitenStyles = computed(() => {
  const intensity = Math.min(props.whitenIntensity, 100) / 100
  return {
    backgroundColor: props.whitenColor,
    opacity: intensity.toString()
  }
})

// 渐变叠加样式
const gradientStyles = computed(() => {
  let gradientDirection = props.gradientDirection

  const gradient = `linear-gradient(${gradientDirection}, ${props.gradientColors.join(', ')})`
  
  return {
    background: gradient
  }
})

// 背景容器样式
const backgroundStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.parallax) {
    styles.transform = `translateY(calc(var(--scroll-y) * ${props.parallaxIntensity}px))`
  }
  
  return styles
})
</script>

<style scoped lang="scss">
.app-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1; // 确保背景在内容后面

  // 固定背景
  &.fixed-background {
    position: fixed;
  }

  // 视差效果
  &.parallax-background {
    will-change: transform;
    transition: transform 0.1s linear;
  }

  // 所有层共用样式
  .background-image,
  .fog-layer,
  .whiten-layer,
  .gradient-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  // 背景图片层
  .background-image {
    z-index: 1;
  }

  // 雾化效果层
  .fog-layer {
    z-index: 2;
    backdrop-filter: blur(2px); // 额外的雾化效果
  }

  // 白化效果层
  .whiten-layer {
    z-index: 3;
    mix-blend-mode: overlay; // 使用混合模式增强效果
  }

  // 渐变叠加层
  .gradient-overlay {
    z-index: 4;
    mix-blend-mode: soft-light; // 柔和的混合模式
  }

  // 响应式设计
  @media (max-width: 768px) {
    .background-image {
      background-position: center center;
    }
  }

  // 打印时隐藏背景
  @media print {
    display: none;
  }
}

// 全局样式，用于视差效果
:global(html) {
  --scroll-y: 0;
}
</style>