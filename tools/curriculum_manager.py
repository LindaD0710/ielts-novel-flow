#!/usr/bin/env python3
"""
IELTS Novel Flow - 课程管理器
负责智能选词、进度追踪和学习管理
"""

import json
import os
import random
from typing import List, Dict, Optional, Set

# 获取脚本所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROGRESS_FILE = os.path.join(BASE_DIR, "progress_tracker.json")
IELTS_SOURCE_FILE = os.path.join(BASE_DIR, "ielts_source.json")


def get_progress_file_for_category(category_id: str) -> str:
    """
    根据分类ID获取对应的进度文件路径
    
    Args:
        category_id: 分类ID（如 "reborn", "suspense", "romance", "business"）
    
    Returns:
        进度文件路径
    """
    if not category_id:
        return PROGRESS_FILE  # 默认全局进度文件
    
    filename = f"progress_tracker_{category_id}.json"
    return os.path.join(BASE_DIR, filename)


class CurriculumManager:
    """课程管理器类"""

    def __init__(self, progress_file: str = PROGRESS_FILE):
        """
        初始化课程管理器
        
        Args:
            progress_file: 进度追踪文件路径
        """
        self.progress_file = progress_file
        self.progress = self._load_progress()

    def _load_progress(self) -> Dict:
        """加载进度追踪文件"""
        if not os.path.exists(self.progress_file):
            # 如果文件不存在，从词源文件初始化
            self._initialize_from_source()
        
        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                progress = json.load(f)
                # 兼容旧进度文件：补齐 assigned_words 字段
                if isinstance(progress, dict) and "assigned_words" not in progress:
                    progress["assigned_words"] = []
                    self._save_progress(progress)
                return progress
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️  警告：无法加载进度文件 {self.progress_file}: {e}")
            self._initialize_from_source()
            return self._load_progress()

    def _initialize_from_source(self):
        """从词源文件初始化进度追踪"""
        if not os.path.exists(IELTS_SOURCE_FILE):
            raise FileNotFoundError(
                f"词源文件 {IELTS_SOURCE_FILE} 不存在，请先创建词源文件"
            )
        
        with open(IELTS_SOURCE_FILE, "r", encoding="utf-8") as f:
            source_words = json.load(f)
        
        # 去重
        unique_words = list(set(source_words))
        
        progress = {
            "total_words": len(unique_words),
            "learned_words": [],
            "pending_words": unique_words,
            "assigned_words": [],  # 已分配但未完成的单词（用于 step1 到 step2 之间的状态）
            "current_book_chapter": 1,
        }
        
        self._save_progress(progress)
        print(f"✅ 已从 {IELTS_SOURCE_FILE} 初始化进度追踪，共 {len(unique_words)} 个单词")

    def _save_progress(self, progress: Optional[Dict] = None):
        """保存进度追踪文件"""
        if progress is None:
            progress = self.progress
        
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

    def get_next_batch(
        self,
        batch_size: int = 20,
        mark_as_assigned: bool = True,
        prefer_pool: Optional[List[str]] = None,
    ) -> List[str]:
        """
        获取下一批新单词（从待学习列表中按顺序取出）
        - 如果提供 prefer_pool，则会优先从 pool 中抽取（补漏），不够再从 pending 补齐
        
        Args:
            batch_size: 批次大小，默认 20 个单词
            mark_as_assigned: 是否立即标记为"已分配"（从 pending_words 移除），默认 True
            prefer_pool: 优先词池（如 missing_ielts_words.txt）
        
        Returns:
            新单词列表
        """
        pending = self.progress.get("pending_words", [])

        # 规范化 pool
        pool_set: Set[str] = set()
        if prefer_pool:
            for w in prefer_pool:
                if isinstance(w, str):
                    ww = w.strip().lower()
                    if ww:
                        pool_set.add(ww)

        # 1) 优先从 pool 抽（保持 pending 的顺序）
        batch: List[str] = []
        if pool_set:
            for w in pending:
                if w.lower() in pool_set:
                    batch.append(w)
                    if len(batch) >= batch_size:
                        break

        # 2) 不够则从 pending 补齐（仍保持顺序）
        if len(batch) < batch_size:
            batch_lc = set([b.lower() for b in batch])
            for w in pending:
                if w.lower() in batch_lc:
                    continue
                batch.append(w)
                if len(batch) >= batch_size:
                    break

        if len(batch) < batch_size:
            print(f"⚠️  提示：待学习单词不足 {batch_size} 个，仅返回 {len(batch)} 个")
        
        # 如果标记为已分配，立即从 pending_words 中移除，避免重复分配
        if mark_as_assigned and batch:
            # 从待学习列表中移除
            new_pending = [w for w in pending if w.lower() not in [b.lower() for b in batch]]
            assigned = self.progress.get("assigned_words", [])
            # 添加到已分配列表（避免重复）
            new_assigned = list(set([w.lower() for w in assigned] + [b.lower() for b in batch]))
            
            self.progress["pending_words"] = new_pending
            self.progress["assigned_words"] = [w for w in assigned if w.lower() in new_assigned] + [b for b in batch if b.lower() not in [a.lower() for a in assigned]]
            self._save_progress()
            
            print(f"💡 已标记 {len(batch)} 个单词为'已分配'，避免重复使用")
        
        return batch

    def get_review_batch(self, batch_size: int = 5) -> List[str]:
        """
        获取复习单词（从已学习列表中随机取出）
        
        Args:
            batch_size: 批次大小，默认 5 个单词
        
        Returns:
            复习单词列表
        """
        learned = self.progress.get("learned_words", [])
        
        if len(learned) < batch_size:
            # 如果已学习单词不足，返回全部
            print(f"⚠️  提示：已学习单词不足 {batch_size} 个，返回全部 {len(learned)} 个")
            return learned
        
        # 随机选择
        return random.sample(learned, batch_size)

    def mark_as_learned(self, word_list: List[str]):
        """
        标记单词为已学习（从已分配列表中移除，添加到已学习列表）
        
        Args:
            word_list: 要标记的单词列表
        """
        if not word_list:
            return
        
        # 转换为小写并去重
        word_list = list(set([w.lower().strip() for w in word_list if w]))
        
        pending = self.progress.get("pending_words", [])
        learned = self.progress.get("learned_words", [])
        assigned = self.progress.get("assigned_words", [])
        
        # 从待学习列表中移除（如果还在的话）
        new_pending = [w for w in pending if w.lower() not in [wl.lower() for wl in word_list]]
        
        # 从已分配列表中移除（这些单词已经完成了）
        new_assigned = [w for w in assigned if w.lower() not in [wl.lower() for wl in word_list]]
        
        # 添加到已学习列表（避免重复）
        new_learned = list(set(learned + word_list))
        
        # 更新进度
        self.progress["pending_words"] = new_pending
        self.progress["assigned_words"] = new_assigned
        self.progress["learned_words"] = new_learned
        self.progress["total_words"] = len(new_learned) + len(new_pending) + len(new_assigned)
        
        # 保存
        self._save_progress()
        
        print(f"✅ 已标记 {len(word_list)} 个单词为已学习")
        print(f"   待学习：{len(new_pending)} 个，已分配：{len(new_assigned)} 个，已学习：{len(new_learned)} 个")

    def increment_chapter(self):
        """增加章节计数"""
        self.progress["current_book_chapter"] = self.progress.get("current_book_chapter", 0) + 1
        self._save_progress()

    def get_current_chapter(self) -> int:
        """获取当前章节号"""
        return self.progress.get("current_book_chapter", 1)

    def get_statistics(self) -> Dict:
        """获取学习统计信息"""
        total = self.progress.get("total_words", 0)
        learned = len(self.progress.get("learned_words", []))
        pending = len(self.progress.get("pending_words", []))
        assigned = len(self.progress.get("assigned_words", []))
        progress_percent = (learned / total * 100) if total > 0 else 0
        
        return {
            "total_words": total,
            "learned_words": learned,
            "pending_words": pending,
            "assigned_words": assigned,
            "progress_percent": round(progress_percent, 2),
            "current_chapter": self.progress.get("current_book_chapter", 1),
        }

    def print_statistics(self):
        """打印学习统计信息"""
        stats = self.get_statistics()
        print("\n" + "=" * 50)
        print("📊 学习进度统计")
        print("=" * 50)
        print(f"总词汇量：{stats['total_words']} 个")
        print(f"已学习：{stats['learned_words']} 个")
        print(f"待学习：{stats['pending_words']} 个")
        if stats.get('assigned_words', 0) > 0:
            print(f"已分配（进行中）：{stats['assigned_words']} 个")
        print(f"学习进度：{stats['progress_percent']}%")
        print(f"当前章节：第 {stats['current_chapter']} 章")
        print("=" * 50 + "\n")


# ==================== 便捷函数 ====================

def get_curriculum_manager(progress_file: str = PROGRESS_FILE) -> CurriculumManager:
    """获取课程管理器实例"""
    return CurriculumManager(progress_file)


if __name__ == "__main__":
    # 测试代码
    manager = CurriculumManager()
    
    # 打印统计信息
    manager.print_statistics()
    
    # 获取下一批单词
    print("获取下一批新单词（20个）：")
    next_batch = manager.get_next_batch(20)
    print(next_batch)
    print()
    
    # 获取复习单词
    print("获取复习单词（5个）：")
    review_batch = manager.get_review_batch(5)
    print(review_batch)
    print()
    
    # 模拟标记为已学习
    if next_batch:
        print("模拟标记前5个单词为已学习：")
        manager.mark_as_learned(next_batch[:5])
        manager.print_statistics()

