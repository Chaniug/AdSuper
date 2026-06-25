import logging
import time
import random
from datetime import datetime
from typing import Optional, Callable, Any
from functools import wraps

# 全局日志配置
_logging_configured = False
_logger = None

# GitHub API 重试配置
MAX_RETRIES = 5
BASE_DELAY = 2  # 基础延迟（秒）
MAX_DELAY = 60  # 最大延迟（秒）

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
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}")
        except Exception:
            # 降级 print 也失败时，静默处理避免日志本身导致崩溃
            pass
        return
    
    # 使用 logging 模块
    try:
        log_level = getattr(logging, level.upper(), logging.INFO)
        _logger.log(log_level, message)
    except Exception:
        pass

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

def exponential_backoff(retry_count: int) -> float:
    """
    计算指数退避延迟时间
    
    Args:
        retry_count: 当前重试次数
        
    Returns:
        延迟时间（秒）
    """
    delay = min(BASE_DELAY * (2 ** retry_count), MAX_DELAY)
    # 添加随机抖动，避免惊群效应
    jitter = delay * 0.1 * random.random()
    return delay + jitter

def retry_on_exception(
    max_retries: int = MAX_RETRIES,
    exceptions: tuple = (Exception,),
    should_retry: Callable[[Exception], bool] = None
):
    """
    重试装饰器 - 在出现异常时自动重试
    
    Args:
        max_retries: 最大重试次数
        exceptions: 需要捕获的异常类型
        should_retry: 判断是否应该重试的函数（可选）
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    # 判断是否应该重试
                    if should_retry and not should_retry(e):
                        raise e
                    
                    # 如果是最后一次尝试，抛出异常
                    if attempt == max_retries:
                        log(f"重试 {max_retries} 次后仍然失败: {e}", "ERROR")
                        raise e
                    
                    # 计算延迟时间
                    delay = exponential_backoff(attempt)
                    log(f"第 {attempt + 1} 次尝试失败: {e}", "WARNING")
                    log(f"{delay:.1f} 秒后重试...", "INFO")
                    time.sleep(delay)
            
            # 理论上不会到达这里
            raise last_exception
        
        return wrapper
    return decorator

def is_github_api_error_retryable(error: Exception) -> bool:
    """
    判断 GitHub API 错误是否可重试
    
    Args:
        error: 异常对象
        
    Returns:
        是否可重试
    """
    error_str = str(error).lower()
    
    # 速率限制错误 - 可重试
    if 'rate limit' in error_str or '403' in error_str:
        return True
    
    # 网络超时 - 可重试
    if 'timeout' in error_str or 'connection' in error_str:
        return True
    
    # 服务器错误 - 可重试
    if '502' in error_str or '503' in error_str or '504' in error_str:
        return True
    
    # 其他错误 - 不重试
    return False

def handle_github_rate_limit(github_obj) -> None:
    """
    处理 GitHub API 速率限制（Core + Search）
    Search API 限制更严格（30次/分钟），需优先检查

    Args:
        github_obj: PyGithub Github 对象
    """
    try:
        rate_limit = github_obj.get_rate_limit()

        # 1) 优先检查 Search API（限制: 30次/分钟，最易耗尽）
        search_limit = rate_limit.search
        if search_limit.remaining < 5:
            reset_time = search_limit.reset
            wait_seconds = max(0, (reset_time - datetime.now(reset_time.tzinfo)).total_seconds())
            log(f"⚠️  GitHub Search API 速率限制即将用尽，剩余: {search_limit.remaining}", "WARNING")
            if wait_seconds < 120:
                log(f"自动等待 {wait_seconds:.0f} 秒...", "INFO")
                time.sleep(wait_seconds + 2)

        # 2) 再检查 Core API（限制: 5000次/小时）
        core_limit = rate_limit.core
        if core_limit.remaining < 10:
            reset_time = core_limit.reset
            wait_seconds = max(0, (reset_time - datetime.now(reset_time.tzinfo)).total_seconds())

            if wait_seconds > 0:
                log(f"⚠️  GitHub API 速率限制即将用尽，剩余: {core_limit.remaining}", "WARNING")
                log(f"将在 {wait_seconds:.0f} 秒后重置，建议等待...", "WARNING")

                # 如果等待时间不长，自动等待
                if wait_seconds < 300:  # 小于5分钟
                    log(f"自动等待 {wait_seconds:.0f} 秒...", "INFO")
                    time.sleep(wait_seconds + 5)  # 多等5秒确保重置
    except Exception as e:
        log(f"检查速率限制失败: {e}", "WARNING")

def load_rules_from_file(filename: str, skip_comments: bool = True) -> set:
    """
    从文件中加载规则（公共函数）
    
    Args:
        filename: 规则文件名
        skip_comments: 是否跳过注释行（以 ! 开头）
        
    Returns:
        规则字符串集合
    """
    rules = set()
    
    from pathlib import Path
    if not Path(filename).exists():
        log(f"❌ 找不到文件: {filename}", "ERROR")
        return rules
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行
                if not line:
                    continue
                # 根据需要跳过注释
                if skip_comments and line.startswith('!'):
                    continue
                rules.add(line)
    except Exception as e:
        log(f"❌ 读取文件失败 {filename}: {e}", "ERROR")
    
    return rules
