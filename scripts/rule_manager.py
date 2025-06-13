import os
from datetime import datetime
from typing import List
from .rule_validator import Rule, RuleValidator
from .utils import log

class RuleManager:
    """规则管理器"""

    def __init__(self, base_dir: str = '.'):
        """
        初始化规则管理器

        Args:
            base_dir: 基础目录
        """
        self.base_dir = base_dir
        self.validator = RuleValidator()
        self.merged_rules_dir = os.path.join(base_dir, 'merged_rules')
        os.makedirs(self.merged_rules_dir, exist_ok=True)

    def load_existing_rules(self, filename: str) -> List[Rule]:
        """
        加载现有规则

        Args:
            filename: 规则文件名

        Returns:
            规则列表
        """
        rules = []
        file_path = os.path.join(self.base_dir, filename)
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('!'):
                    is_valid, content, rule_type = self.validator.validate_rule(line, i)
                    if is_valid and content:
                        rules.append(Rule(
                            content=content,
                            type=rule_type,
                            line_number=i,
                            source="existing",
                            created_at=datetime.now()
                        ))
        return rules

    def merge_rules(self, new_rules: List[Rule], base_filename: str = 'AdSuper.txt') -> str:
        """
        合并规则并优化，返回新文件名

        Args:
            new_rules: 新规则列表（必须是Rule对象列表）
            base_filename: 基础规则文件名

        Returns:
            新规则文件名
        """
        existing_rules = self.load_existing_rules(base_filename)
        log(f"现有规则数: {len(existing_rules)}，新规则数: {len(new_rules)}")
        all_rules = existing_rules + new_rules
        unique_rules = []
        seen = set()
        for rule in all_rules:
            normalized = rule.content.strip()
            if not normalized:
                continue
            if normalized not in seen:
                seen.add(normalized)
                if normalized.startswith('!') and not normalized.startswith('! '):
                    normalized = '! ' + normalized[1:]
                rule.content = normalized
                unique_rules.append(rule)
        conflicts = self.validator.check_conflicts(unique_rules)
        if conflicts:
            log("\n发现规则冲突：")
            for rule1, rule2, message in conflicts:
                log(f"- {message}")
                log(f"  来源1: {rule1.source}")
                log(f"  来源2: {rule2.source}")
        sorted_rules = self.validator.sort_rules(unique_rules)
        new_filename = 'adnew.txt'
        self._save_rules(sorted_rules, os.path.join(self.base_dir, new_filename))
        log(f"已写入合并规则到 {new_filename}")
        # 备份
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.merged_rules_dir, f'AdSuper_backup_{timestamp}.txt')
        self._save_rules(sorted_rules, backup_file)
        # 保留最新3个备份
        backup_files = sorted(
            [f for f in os.listdir(self.merged_rules_dir)
             if f.startswith('AdSuper_backup_') and f.endswith('.txt')],
            key=lambda x: os.path.getmtime(os.path.join(self.merged_rules_dir, x)),
            reverse=True
        )
        for old_backup in backup_files[3:]:
            try:
                os.remove(os.path.join(self.merged_rules_dir, old_backup))
            except Exception as e:
                log(f"删除备份文件失败: {old_backup}, 错误: {e}")
        return new_filename

    def _save_rules(self, rules: List[Rule], filename: str):
        """
        保存规则到文件

        Args:
            rules: 规则列表
            filename: 文件名（含路径）
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"! AdSuper 规则文件\n")
                f.write(f"! 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"! 规则总数: {len(rules)}\n\n")
                rules_by_type = {}
                for rule in rules:
                    if rule.type not in rules_by_type:
                        rules_by_type[rule.type] = []
                    rules_by_type[rule.type].append(rule)
                for rule_type in self.validator.priority_order:
                    if rule_type in rules_by_type:
                        f.write(f"\n! {rule_type.value.upper()} 规则 ({len(rules_by_type[rule_type])}条)\n")
                        for rule in rules_by_type[rule_type]:
                            if rule.source and rule.source != "existing":
                                f.write(f"! 来源: {rule.source}\n")
                            f.write(f"{rule.content}\n")
        except Exception as e:
            log(f"保存规则文件失败: {filename}, 错误: {e}")
