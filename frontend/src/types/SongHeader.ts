export interface SongHeader{
  song_id: number,
  title: string,
  diff: number[],
  jacket_name: string,
  band_id: number,
}

export const DEAULT_SONG_HEADER: SongHeader = {
  song_id: -1,
  title: '',
  diff: [-1, -1, -1, -1, -1],
  jacket_name: '',
  band_id: -1
};