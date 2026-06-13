import logging
from datetime import datetime
from typing import Optional

# 全局日志配置
_logging_configured = False
_logger = None

def setup_logging(level: str = "INFO", log_file: Optional[str] = None, verbose: bool = False):
    """
    配置日志系统
    
    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
        log_file: 日志文件路径（可选）
        verbose: 是否详细输出（DEBUG 级别）
    """
    global _logging_configured, _logger
    
    if _logging_configured:
        return
    
    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    if verbose:
        log_level = logging.DEBUG
    
    # 创建 logger
    _logger = logging.getLogger('adsuper')
    _logger.setLevel(log_level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # 添加控制台处理器
    _logger.addHandler(console_handler)
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            _logger.addHandler(file_handler)
        except Exception as e:
            print(f"警告：无法创建日志文件 {log_file}: {e}")
    
    _logging_configured = True

def log(message: str, level: str = "INFO"):
    """
    统一日志输出（增强版）
    
    Args:
        message: 日志消息
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
    """
    global _logger
    
    # 如果日志系统未配置，使用简单的打印输出（保持向后兼容）
    if not _logging_configured:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}")
        return
    
    # 使用 logging 模块
    log_level = getattr(logging, level.upper(), logging.INFO)
    _logger.log(log_level, message)

def set_log_level(level: str):
    """
    动态设置日志级别
    
    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
    """
    global _logger
    if _logger:
        log_level = getattr(logging, level.upper(), logging.INFO)
        _logger.setLevel(log_level)
        for handler in _logger.handlers:
            handler.setLevel(log_level)

# 为了保持完全向后兼容，提供一个简单的 log 函数（不带级别）
# 所有现有代码都应该继续工作
# 新代码可以使用 log(message, level="DEBUG") 来指定级别
