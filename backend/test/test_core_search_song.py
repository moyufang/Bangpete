import pytest
import json
from unittest.mock import mock_open, patch

from configuration import *
from core.search.song import SongConstraint, SongsHeader, MAIN_BANG

class TestSongConstraint:
    """测试SongConstraint模型验证"""
    
    def test_valid_constraint(self):
        """测试有效约束条件"""
        constraint = SongConstraint(
            diff=2,
            level_low=10,
            level_high=20,
            band_id=1
        )
        assert constraint.diff == 2
        assert constraint.level_low == 10
        assert constraint.level_high == 20
        assert constraint.band_id == 1
    
    def test_diff_boundary(self):
        """测试难度索引边界值"""
        # 测试下限
        constraint = SongConstraint(diff=-1, level_low=1, level_high=10, band_id=1)
        assert constraint.diff == 0
        
        # 测试上限
        constraint = SongConstraint(diff=5, level_low=1, level_high=10, band_id=1)
        assert constraint.diff == 4
        
        # 测试正常范围
        for diff in range(0, 5):
            constraint = SongConstraint(diff=diff, level_low=1, level_high=10, band_id=1)
            assert constraint.diff == diff
    
    def test_level_boundary(self):
        """测试难度等级边界值"""
        # 测试下限
        constraint = SongConstraint(diff=0, level_low=-1, level_high=50, band_id=1)
        assert constraint.level_low == 0
        
        # 测试上限
        constraint = SongConstraint(diff=0, level_low=1, level_high=60, band_id=1)
        assert constraint.level_high == 50
    
    def test_level_consistency(self):
        """测试难度范围一致性"""
        # 当level_low > level_high时，应该自动调整
        constraint = SongConstraint(diff=0, level_low=20, level_high=10, band_id=1)
        assert constraint.level_low == constraint.level_high
    
    def test_band_id_validation(self):
        """测试乐队ID验证"""
        # 主乐队ID应该保持不变
        for band_id in MAIN_BANG:
            constraint = SongConstraint(diff=0, level_low=1, level_high=10, band_id=band_id)
            assert constraint.band_id == band_id
        
        # 非主乐队ID应该被转换为-1
        constraint = SongConstraint(diff=0, level_low=1, level_high=10, band_id=99)
        assert constraint.band_id == -1
    
    def test_pagination_validation(self):
        """测试分页参数验证"""
        # 测试小于1的值被修正
        constraint = SongConstraint(
            diff=0, level_low=1, level_high=10, band_id=1,
            start_count=0, page_size=0
        )
        assert constraint.start_count == 1
        assert constraint.page_size == 1

class TestSongsHeader:
    """测试SongsHeader类功能"""
    
    @pytest.fixture
    def sample_songs_data(self):
        """提供测试用的歌曲数据"""
        return {
            "1": {
                "song_id": 1,
                "title": "Test Song 1",
                "diff": [5, 10, 15, 20, -1],
                "jacket_name": "test1",
                "band_id": 1
            },
            "2": {
                "song_id": 2,
                "title": "Test Song 2",
                "diff": [7, 12, 18, 25, 30],
                "jacket_name": "test2",
                "band_id": 2
            },
            "3": {
                "song_id": 3,
                "title": "Test Song 3",
                "diff": [3, 8, 13, 19, -1],
                "jacket_name": "test3",
                "band_id": 99  # 非主乐队
            },
            "4": {
                "song_id": 4,
                "title": "Test Song 4",
                "diff": [10, 15, 22, 28, 35],
                "jacket_name": "test4",
                "band_id": 18
            }
        }
    
    @pytest.fixture
    def songs_header(self, sample_songs_data):
        """创建SongsHeader实例"""
        header = SongsHeader(sample_songs_data)
        header.build()
        return header
    
    def test_build_index_structure(self, songs_header, sample_songs_data):
        """测试索引构建结构"""
        # 检查索引包含所有MAIN_BAND和难度级别
        for band_id in MAIN_BANG:
            assert band_id in songs_header.tree
            for diff in range(5):
                assert diff in songs_header.tree[band_id]
        
        # 检查特定歌曲是否被正确索引
        song1 = sample_songs_data["1"]
        # 歌曲1应该在band_id=1和band_id=0的索引中
        for band_id in [1, 0]:
            for diff, level in enumerate(song1["diff"]):
                if level != -1:
                    assert (level, 1) in songs_header.tree[band_id][diff]
        
        # 非主乐队歌曲应该在band_id=-1的索引中
        song3 = sample_songs_data["3"]
        for diff, level in enumerate(song3["diff"]):
            if level != -1:
                assert (level, 3) in songs_header.tree[-1][diff]
    
    def test_get_songs_by_band(self, songs_header):
        """测试按乐队查询"""
        constraint = SongConstraint(diff=0, level_low=1, level_high=50, band_id=1)
        result, exhausted = songs_header.get_songs(constraint)
        
        # 应该只返回band_id=1的歌曲
        assert len(result) == 1
        assert "1" in result
        assert result["1"]["title"] == "Test Song 1"
    
    def test_get_songs_by_difficulty_range(self, songs_header):
        """测试按难度范围查询"""
        constraint = SongConstraint(diff=0, level_low=5, level_high=10, band_id=0)
        result, exhausted = songs_header.get_songs(constraint)
        
        # 应该返回难度在5-10之间的歌曲
        assert len(result) >= 1
        for song_id, song in result.items():
            level = song["diff"][constraint.diff]
            assert constraint.level_low <= level <= constraint.level_high
    
    def test_get_songs_by_non_main_band(self, songs_header):
        """测试查询非主乐队歌曲"""
        constraint = SongConstraint(diff=0, level_low=1, level_high=50, band_id=-1)
        result, exhausted = songs_header.get_songs(constraint)
        
        # 应该只返回非主乐队歌曲
        assert len(result) == 1
        assert "3" in result
        assert result["3"]["band_id"] == 99
    
    def test_get_songs_pagination(self, songs_header):
        """测试分页功能"""
        # 第一页
        constraint1 = SongConstraint(
            diff=0, level_low=1, level_high=50, band_id=0,
            start_count=1, page_size=2
        )
        result1, exhausted1 = songs_header.get_songs(constraint1)
        
        # 第二页
        constraint2 = SongConstraint(
            diff=0, level_low=1, level_high=50, band_id=0,
            start_count=3, page_size=2
        )
        result2, exhausted2 = songs_header.get_songs(constraint2)
        
        # 两页结果应该不重复
        common_ids = set(result1.keys()) & set(result2.keys())
        assert len(common_ids) == 0
    
    def test_get_songs_with_nonexistent_band_in_tree(self, songs_header):
        """测试查询树中不存在的乐队"""
        # 临时修改tree，移除一个乐队
        original_band_id = MAIN_BANG[0]
        if original_band_id in songs_header.tree:
            del songs_header.tree[original_band_id]
        
        constraint = SongConstraint(
            diff=0, level_low=1, level_high=50, band_id=original_band_id
        )
        result, exhausted = songs_header.get_songs(constraint)
        
        assert len(result) == 0
        assert exhausted is True

class TestIntegration:
  """集成测试"""
  
  def test_file_loading_integration(self):
    """测试文件加载集成"""
    mock_data = {
        "1": {
            "song_id": 1,
            "title": "Integration Test Song",
            "diff": [5, 10, 15, 20, -1],
            "jacket_name": "integration_test",
            "band_id": 1
        }
    }
      
    # 模拟文件读取
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))) as mock_file:
      with patch('core.search.song.SONGS_HEADER_PATH', 'dummy_path.json'):
        # 重新导入模块以触发文件加载
        import importlib
        import core.search.song as song_module
        importlib.reload(song_module)
        
        # 验证数据加载
        assert hasattr(song_module, 'songs_header')

if __name__ == "__main__":
    pytest.main([__file__, "-v"])