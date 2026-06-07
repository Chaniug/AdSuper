from datetime import datetime

def log(message: str):
    """
    统一日志输出
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
