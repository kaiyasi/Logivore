"""
Utility functions for Logivore
"""
import datetime
from utils.i18n import i18n

def get_bar(percent: float, length: int = 20) -> str:
    """Generate a progress bar string"""
    filled_len = int(length * percent / 100)
    bar = '█' * filled_len + '─' * (length - filled_len)
    return f"[{bar}]"

def format_bytes(byte_count: int) -> str:
    """Format byte count to human readable string"""
    if byte_count is None:
        return "0 B"

    power = 1024
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}

    while byte_count >= power and n < len(power_labels) - 1:
        byte_count /= power
        n += 1

    return f"{byte_count:.2f} {power_labels[n]}B"

def format_uptime(seconds: float) -> str:
    """Format uptime seconds to human readable string"""
    days, rem = divmod(int(seconds), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def get_core_bars(per_cpu_percent: list) -> str:
    """Generate CPU core usage bars"""
    if not per_cpu_percent or len(per_cpu_percent) > 20:
        return ""

    core_bars_list = []
    for percent in per_cpu_percent:
        if percent < 10:
            bar_char = " "
        elif percent < 30:
            bar_char = "▂"
        elif percent < 50:
            bar_char = "▄"
        elif percent < 70:
            bar_char = "▆"
        else:
            bar_char = "█"
        core_bars_list.append(bar_char)

    return f"{i18n.t('system.cores')} : [{''.join(core_bars_list)} ]"
