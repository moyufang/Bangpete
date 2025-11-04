// frontend/src/services/get.ts
import axios from 'axios';
import { BACKEND_ADDRESS } from '@/config';

// 定义类型
export interface SongHeader {
  song_id: number;
  title: string;
  diff: number[];
  jacket_name: string;
  band_id: number;
}

export interface SearchResult {
  id: string;
  header: SongHeader;
  error?: string;
}

export interface SongConstraint {
  diff: number;
  level_low: number;
  level_high: number;
  band_id: number;
  start_count?: number;
  page_size?: number;
}

export interface SongListResult {
  sub_songs_header: Record<string, SongHeader>;
  is_exhausted: boolean;
}

export default {
  // 获取header文件
  async getHeaderFile(fileName: string): Promise<Blob> {
    const response = await axios.get(`${BACKEND_ADDRESS}/data/header/${fileName}`, {
      responseType: 'blob'
    });
    return response.data;
  },

  // 获取jacket文件
  async getJacketFile(fileName: string): Promise<Blob> {
    const response = await axios.get(`${BACKEND_ADDRESS}/data/jacket/${fileName}`, {
      responseType: 'blob'
    });
    return response.data;
  },

  // 搜索歌曲
  async searchSong(q: string, way: string = 'unknown'): Promise<SearchResult> {
    const response = await axios.get(`${BACKEND_ADDRESS}/core/search/song/`, {
      params: { q, way }
    });
    return response.data;
  },

  // 获取歌曲列表
  async getSongList(constraint: SongConstraint): Promise<SongListResult> {
    const response = await axios.get(`${BACKEND_ADDRESS}/core/search/song/list/`, {
      params: constraint
    });
    return response.data;
  }
};