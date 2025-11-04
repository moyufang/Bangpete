import { defineStore } from 'pinia'

interface ResourceCache {
  json: Map<string, any>
  images: Map<string, string>
  loading: Set<string>
  errors: Map<string, string>
}

export const useLobbyStore = defineStore('lobby', {
  state: (): ResourceCache => ({
    json: new Map(),
    images: new Map(),
    loading: new Set(),
    errors: new Map()
  }),

  getters: {
    //example: "header/songs_header.json"
    getJsonData: (state) => (fileName: string) => {
      return state.json.get(fileName)
    },
    
    getImageUrl: (state) => (fileName: string) => {
      return state.images.get(fileName)
    },
    
    isLoading: (state) => (resourceKey: string) => {
      return state.loading.has(resourceKey)
    },
    
    getError: (state) => (resourceKey: string) => {
      return state.errors.get(resourceKey)
    }
  },

  actions: {
    async fetchJsonResource(fileName: string) {
      const resourceKey = `json:${fileName}`
      
      // 检查缓存
      if (this.json.has(fileName)) {
        return this.json.get(fileName)
      }
      
      // 检查是否正在加载
      if (this.loading.has(resourceKey)) {
        return null
      }
      
      // 清除之前的错误
      this.errors.delete(resourceKey)
      this.loading.add(resourceKey)
      
      try {
        const response = await fetch(`http://127.0.0.1:8888/data/header/${fileName}`)
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        
        const data = await response.json()
        this.json.set(fileName, data)
        return data
        
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : 'Unknown error'
        this.errors.set(resourceKey, errorMsg)
        throw error
      } finally {
        this.loading.delete(resourceKey)
      }
    },
    
    async fetchImageResource(fileName: string) {
      const resourceKey = `image:${fileName}`
      
      // 检查缓存
      if (this.images.has(fileName)) {
        return this.images.get(fileName)
      }
      
      // 检查是否正在加载
      if (this.loading.has(resourceKey)) {
        return null
      }
      
      // 清除之前的错误
      this.errors.delete(resourceKey)
      this.loading.add(resourceKey)
      
      try {
        const response = await fetch(`http://127.0.0.1:8888/data/jacket/${fileName}`)
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        
        const blob = await response.blob()
        const imageUrl = URL.createObjectURL(blob)
        this.images.set(fileName, imageUrl)
        return imageUrl
        
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : 'Unknown error'
        this.errors.set(resourceKey, errorMsg)
        throw error
      } finally {
        this.loading.delete(resourceKey)
      }
    },
    
    // 预加载多个资源
    async preloadResources(jsonFiles: string[] = [], imageFiles: string[] = []) {
      const promises = []
      
      for (const jsonFile of jsonFiles) {
        promises.push(this.fetchJsonResource(jsonFile))
      }
      
      for (const imageFile of imageFiles) {
        promises.push(this.fetchImageResource(imageFile))
      }
      
      return Promise.allSettled(promises)
    },
    
    // 清理缓存
    clearCache() {
      // 释放 Blob URLs 防止内存泄漏
      for (const url of this.images.values()) {
        URL.revokeObjectURL(url)
      }
      
      this.json.clear()
      this.images.clear()
      this.errors.clear()
    }
  }
})