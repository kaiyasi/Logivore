"""
Enhanced logging configuration for Logivore
Provides colored console output and structured logging
"""
import logging
import sys
import os
from datetime import datetime
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m',      # Reset
        'BOLD': '\033[1m',       # Bold
        'DIM': '\033[2m',        # Dim
    }

    # Emoji prefixes
    EMOJIS = {
        'DEBUG': '🔍',
        'INFO': '📋',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨',
    }

    def __init__(self, use_colors: bool = True, use_emojis: bool = True):
        self.use_colors = use_colors and self._supports_color()
        self.use_emojis = use_emojis
        super().__init__()

    def _supports_color(self) -> bool:
        """Check if terminal supports color output"""
        return (
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
            os.environ.get('TERM') != 'dumb'
        )

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors and emojis"""
        # Create a copy to avoid modifying the original record
        record_copy = logging.makeLogRecord(record.__dict__)

        # Get timestamp
        timestamp = datetime.fromtimestamp(record_copy.created).strftime('%H:%M:%S')

        # Get level info
        level_name = record_copy.levelname
        level_color = self.COLORS.get(level_name, '')
        emoji = self.EMOJIS.get(level_name, '📝') if self.use_emojis else ''

        # Format message
        message = record_copy.getMessage()

        # Get logger name (shortened)
        logger_name = record_copy.name
        if logger_name.startswith('logivore.'):
            logger_name = logger_name[9:]  # Remove 'logivore.' prefix

        # Color coding
        if self.use_colors:
            level_str = f"{level_color}{level_name:<8}{self.COLORS['RESET']}"
            timestamp_str = f"{self.COLORS['DIM']}{timestamp}{self.COLORS['RESET']}"
            logger_str = f"{self.COLORS['DIM']}{logger_name}{self.COLORS['RESET']}"
        else:
            level_str = f"{level_name:<8}"
            timestamp_str = timestamp
            logger_str = logger_name

        # Combine all parts
        parts = [timestamp_str, emoji, level_str]
        if logger_name != 'logivore':
            parts.append(f"[{logger_str}]")
        parts.append(message)

        return " ".join(filter(None, parts))

class BotLogger:
    """Enhanced logging system for the bot"""

    def __init__(self, name: str = "logivore", log_file: Optional[str] = None):
        self.name = name
        self.log_file = log_file
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging with console and file handlers"""
        # Create main logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(use_colors=True, use_emojis=True)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (if specified)
        if self.log_file:
            try:
                # Ensure log directory exists
                log_dir = os.path.dirname(self.log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.warning(f"Could not setup file logging: {e}")

        # Prevent duplicate logs from parent loggers
        self.logger.propagate = False

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get a logger instance"""
        if name:
            return logging.getLogger(f"{self.name}.{name}")
        return self.logger

    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)

    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)

    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)

    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)

def setup_bot_logging(log_file: Optional[str] = "logs/logivore.log") -> BotLogger:
    """Setup enhanced logging for the bot"""
    return BotLogger("logivore", log_file)

def log_startup_banner():
    """Display startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                           Logivore                           ║
║                    System Monitor & Manager                  ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def log_system_info():
    """Log system information"""
    import platform
    import psutil

    logger = logging.getLogger("logivore")

    logger.info("=== System Information ===")
    logger.info(f"OS: {platform.system()} {platform.release()}")
    logger.info(f"Python: {platform.python_version()}")
    logger.info(f"CPU Cores: {psutil.cpu_count()}")
    logger.info(f"Memory: {psutil.virtual_memory().total / 1024**3:.1f} GB")
    logger.info("===========================")

def log_cog_status(cog_name: str, status: str, error: Optional[str] = None):
    """Log cog loading status"""
    logger = logging.getLogger("logivore.cogs")

    if status == "loaded":
        logger.info(f"✅ {cog_name}")
    elif status == "failed":
        logger.error(f"❌ {cog_name}: {error}")
    elif status == "reloaded":
        logger.info(f"🔄 {cog_name} reloaded")

def log_performance_stats():
    """Log performance statistics"""
    import psutil
    import os

    logger = logging.getLogger("logivore.performance")

    # Current process stats
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    cpu_percent = process.cpu_percent()

    logger.debug(f"Memory: {memory_mb:.1f} MB | CPU: {cpu_percent:.1f}%")

def log_discord_event(event: str, details: str = ""):
    """Log Discord events"""
    logger = logging.getLogger("logivore.discord")
    logger.info(f"{event} {details}".strip())
