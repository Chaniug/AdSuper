"""
AdSuper 规则同步入口（thin wrapper）

为保持向后兼容，根目录保留此入口文件。
推荐使用 `python -m scripts.sync_issues` 方式运行。
"""

from scripts.sync_issues import main

if __name__ == "__main__":
    main()
