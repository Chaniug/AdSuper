import sys
import os

def load_rules(filename):
    """加载已有规则并去重"""
    if not os.path.exists(filename):
        return set(), []
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    rules = set(line.strip() for line in lines if line.strip() and not line.strip().startswith("!"))
    return rules, lines

def append_rules(filename, new_rules, section="! 新增规则"):
    """将新规则追加到 AdSuper.txt 文件末尾，并加注释分组，自动去重"""
    rules_set, lines = load_rules(filename)
    # 去除已存在的规则
    to_add = [r for r in new_rules if r.strip() and r.strip() not in rules_set]
    if not to_add:
        print("没有需要追加的新规则。")
        return

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{section} {get_today()}\n")
        for rule in to_add:
            f.write(rule.strip() + "\n")
    print(f"{len(to_add)} 条新规则已追加。")

def get_today():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python add_rule.py AdSuper.txt new_rules.txt")
        sys.exit(1)
    ad_file = sys.argv[1]
    new_file = sys.argv[2]
    with open(new_file, "r", encoding="utf-8") as f:
        new_rules = [line.strip() for line in f if line.strip()]
    append_rules(ad_file, new_rules)