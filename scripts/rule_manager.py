"""
规则管理器
负责规则的加载、合并、去重、排序和原子写入保存。
"""

import os
import copy
import tempfile
from datetime import datetime
from typing import List

from .rule_validator import Rule, RuleValidator
from .utils import log
from . import config


class RuleManager:
    """规则管理器"""

    def __init__(self, base_dir: str = '.'):
        """
        初始化规则管理器

        Args:
            base_dir: 基础目录（adnew.txt 生成位置）
        """
        self.base_dir = base_dir
        self.validator = RuleValidator()
        self.merged_rules_dir = os.path.join(base_dir, 'merged_rules')
        os.makedirs(self.merged_rules_dir, exist_ok=True)

    def load_existing_rules(self, filename: str) -> List[Rule]:
        """
        从文件加载现有规则（跳过注释和空行）。

        Args:
            filename: 规则文件名

        Returns:
            Rule 对象列表
        """
        rules: List[Rule] = []
        file_path = os.path.join(self.base_dir, filename) if not os.path.isabs(filename) else filename
        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('!'):
                    result = self.validator.validate_rule(line, i, "existing")
                    if result.is_valid and result.content:
                        rules.append(Rule(
                            content=result.content,
                            type=result.rule_type,
                            line_number=i,
                            source="existing",
                            created_at=datetime.now(),
                        ))
        return rules

    def merge_rules(
        self,
        new_rules: List[Rule],
        base_filename: str = config.BASE_RULES_FILE,
        output_filename: str = config.OUTPUT_FILE,
    ) -> str:
        """
        合并新规则与现有规则，去重、排序后原子写入 output_filename。

        Args:
            new_rules: 新规则列表（Rule 对象）
            base_filename: 基础规则文件路径
            output_filename: 输出规则文件路径

        Returns:
            输出文件名
        """
        existing_rules = self.load_existing_rules(base_filename)
        log(f"现有规则数: {len(existing_rules)}，新规则数: {len(new_rules)}")

        all_rules = existing_rules + new_rules
        unique_rules: List[Rule] = []
        seen = set()

        for rule in all_rules:
            normalized = rule.content.strip()
            if not normalized:
                continue
            # 规范化注释格式（创建副本，不修改原对象）
            if normalized.startswith('!') and not normalized.startswith('! '):
                normalized = '! ' + normalized[1:]
            if normalized not in seen:
                seen.add(normalized)
                new_rule = copy.copy(rule)
                new_rule.content = normalized
                unique_rules.append(new_rule)

        # 冲突检测
        conflicts = self.validator.check_conflicts(unique_rules)
        if conflicts:
            log("\n发现规则冲突：")
            for rule1, rule2, message in conflicts:
                log(f"- {message}")
                log(f"  来源1: {rule1.source}")
                log(f"  来源2: {rule2.source}")

        sorted_rules = self.validator.sort_rules(unique_rules)

        # 原子写入主输出文件
        output_path = output_filename if os.path.isabs(output_filename) \
            else os.path.join(self.base_dir, output_filename)
        self._save_rules_atomic(sorted_rules, output_path)
        log(f"已写入合并规则到 {output_filename}")

        # 备份仅在本地开发环境执行
        if os.environ.get('CI', '').lower() != 'true':
            self._create_backup(sorted_rules)
        else:
            log("CI 环境检测到，跳过本地备份", "DEBUG")

        return output_filename

    def _save_rules_atomic(self, rules: List[Rule], filename: str) -> None:
        """
        原子保存规则到文件。
        先写入临时文件，再通过 os.replace() 原子替换，避免写入中断导致文件损坏。

        Args:
            rules: 规则列表
            filename: 目标文件路径
        """
        # 构造文件内容
        lines = [
            f"! AdSuper 规则文件\n",
            f"! 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"! 规则总数: {len(rules)}\n\n",
        ]

        rules_by_type = {}
        for rule in rules:
            rules_by_type.setdefault(rule.type, []).append(rule)

        for rule_type in self.validator.priority_order:
            if rule_type in rules_by_type:
                lines.append(f"\n! {rule_type.value.upper()} 规则 ({len(rules_by_type[rule_type])}条)\n")
                for rule in rules_by_type[rule_type]:
                    lines.append(f"{rule.content}\n")

        content = ''.join(lines)

        # 原子写入: 临时文件 + os.replace
        file_dir = os.path.dirname(filename) or '.'
        try:
            with tempfile.NamedTemporaryFile(
                mode='w',
                encoding='utf-8',
                dir=file_dir,
                prefix='.tmp_',
                suffix='.txt',
                delete=False,
            ) as tmp_f:
                tmp_f.write(content)
                tmp_path = tmp_f.name

            os.replace(tmp_path, filename)
        except Exception as e:
            # 清理临时文件
            try:
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except OSError:
                pass
            log(f"❌ 保存规则文件失败: {filename}, 错误: {e}", "ERROR")
            raise

    def _create_backup(self, rules: List[Rule]) -> None:
        """创建备份文件，保留最新 3 个。"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.merged_rules_dir, f'AdSuper_backup_{timestamp}.txt')
        try:
            self._save_rules_atomic(rules, backup_file)
        except Exception as e:
            log(f"⚠️  创建备份失败: {e}", "WARNING")
            return

        # 保留最新 3 个备份（按文件名时间戳排序，更可靠）
        backup_files = sorted(
            [f for f in os.listdir(self.merged_rules_dir)
             if f.startswith('AdSuper_backup_') and f.endswith('.txt')],
            reverse=True,
        )
        for old_backup in backup_files[3:]:
            try:
                os.remove(os.path.join(self.merged_rules_dir, old_backup))
            except Exception as e:
                log(f"删除备份文件失败: {old_backup}, 错误: {e}")
