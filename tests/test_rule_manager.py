"""
规则管理器单元测试
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.rule_validator import Rule, RuleType
from scripts.rule_manager import RuleManager


class TestRuleManager:
    """测试 RuleManager 类"""

    def setup_method(self):
        """每个测试使用独立的临时目录"""
        self.tmpdir = tempfile.mkdtemp()
        self.manager = RuleManager(base_dir=self.tmpdir)

    def test_load_existing_rules_empty(self):
        """加载不存在的文件应返回空列表"""
        rules = self.manager.load_existing_rules("nonexistent.txt")
        assert rules == []

    def test_load_existing_rules(self):
        """加载现有规则文件"""
        test_file = os.path.join(self.tmpdir, "test_rules.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("! 注释\n")
            f.write("||example.com^\n")
            f.write("||ads.com^$script\n")
            f.write("\n")  # 空行

        rules = self.manager.load_existing_rules("test_rules.txt")
        assert len(rules) == 2  # 注释和空行被跳过
        assert rules[0].content == "||example.com^"
        assert rules[1].content == "||ads.com^$script"

    def test_merge_rules_creates_output(self):
        """合并规则应生成输出文件"""
        new_rules = [
            Rule(content="||new.com^", type=RuleType.DOMAIN, line_number=1, source="test"),
        ]
        result = self.manager.merge_rules(new_rules, base_filename="empty.txt", output_filename="adnew.txt")
        assert result == "adnew.txt"

        output_path = os.path.join(self.tmpdir, "adnew.txt")
        assert os.path.exists(output_path)

        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "||new.com^" in content
        assert "AdSuper 规则文件" in content

    def test_merge_rules_deduplication(self):
        """重复规则应去重"""
        new_rules = [
            Rule(content="||dup.com^", type=RuleType.DOMAIN, line_number=1, source="test"),
            Rule(content="||dup.com^", type=RuleType.DOMAIN, line_number=2, source="test"),
        ]
        self.manager.merge_rules(new_rules, base_filename="empty.txt", output_filename="out.txt")

        output_path = os.path.join(self.tmpdir, "out.txt")
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content.count("||dup.com^") == 1

    def test_atomic_write_integrity(self):
        """原子写入应保证文件完整性"""
        new_rules = [
            Rule(content="||test.com^", type=RuleType.DOMAIN, line_number=1, source="test"),
        ]
        self.manager.merge_rules(new_rules, base_filename="empty.txt", output_filename="atomic.txt")

        output_path = os.path.join(self.tmpdir, "atomic.txt")
        # 文件应存在且非空
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        # 不应残留临时文件
        tmp_files = [f for f in os.listdir(self.tmpdir) if f.startswith('.tmp_')]
        assert tmp_files == []

    def test_comment_normalization(self):
        """注释格式应规范化（!comment → ! comment）"""
        new_rules = [
            Rule(content="!unformatted", type=RuleType.COMMENT, line_number=1, source="test"),
        ]
        self.manager.merge_rules(new_rules, base_filename="empty.txt", output_filename="norm.txt")

        output_path = os.path.join(self.tmpdir, "norm.txt")
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "! unformatted" in content
        assert "!unformatted" not in content
