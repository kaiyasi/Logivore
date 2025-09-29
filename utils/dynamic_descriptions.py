"""
Dynamic command descriptions that update based on language
"""
from utils.i18n import i18n

def get_desc(key: str) -> str:
    """Get localized description for current language"""
    return i18n.get_text(f"commands.{key}")

# Create command descriptions that will be evaluated at runtime
def monitor_desc():
    return get_desc("monitor_desc")

def ports_desc():
    return get_desc("ports_desc")

def alert_desc():
    return get_desc("alert_desc")

def docker_desc():
    return get_desc("docker_desc")

def reboot_desc():
    return get_desc("reboot_desc")

def recovery_desc():
    return get_desc("recovery_desc")

def config_desc():
    return get_desc("config_desc")

def manage_desc():
    return get_desc("manage_desc")