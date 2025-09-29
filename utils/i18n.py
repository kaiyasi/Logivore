"""
Internationalization (i18n) system for Logivore
Provides multi-language support for all bot text content
"""
import json
import os
from typing import Dict, Any, Optional
import logging

class I18nManager:
    """Manages language files and provides translation functionality"""

    def __init__(self, languages_dir: str = "languages"):
        self.languages_dir = languages_dir
        self.languages: Dict[str, Dict[str, Any]] = {}
        self.default_language = "en"
        self.logger = logging.getLogger("logivore.i18n")

        # Create languages directory if it doesn't exist
        os.makedirs(languages_dir, exist_ok=True)

        # Load all available languages
        self.load_languages()

    def load_languages(self):
        """Load all language files from the languages directory"""
        try:
            language_files = [f for f in os.listdir(self.languages_dir) if f.endswith('.json')]

            for lang_file in language_files:
                lang_code = lang_file[:-5]  # Remove .json extension
                file_path = os.path.join(self.languages_dir, lang_file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.languages[lang_code] = json.load(f)
                    self.logger.info(f"Loaded language: {lang_code}")
                except (json.JSONDecodeError, IOError) as e:
                    self.logger.error(f"Failed to load language file {lang_file}: {e}")

            if not self.languages:
                self.logger.warning("No language files found, creating default English")
                self.create_default_language()

        except OSError as e:
            self.logger.error(f"Failed to access languages directory: {e}")
            self.create_default_language()

    def create_default_language(self):
        """Create default English language file"""
        default_translations = {
            "system": {
                "status": "SYSTEM STATUS",
                "cpu": "CPU",
                "memory": "Memory",
                "swap": "Swap",
                "disk": "Disk",
                "network": "Network",
                "services": "Services",
                "uptime": "Uptime",
                "cores": "Cores",
                "usage": "usage",
                "total_sent": "Total Sent",
                "total_recv": "Recv",
                "listening_ports": "listening ports",
                "docker_containers": "docker containers",
                "no_physical_disks": "No physical disks found",
                "auto_refresh": "Auto-refreshing every {interval} seconds"
            },
            "alerts": {
                "triggered": "🚨 Alert Triggered: {name}",
                "resolved": "✅ Alert Resolved: {name}",
                "current_status": "Current Status",
                "alert_id": "Alert ID",
                "condition_met": "Condition `{target} usage > {threshold}%` was met",
                "condition_not_met": "Condition `{target} usage > {threshold}%` is no longer met",
                "process_not_running": "Monitored process `{target}` was not found running",
                "process_running": "Monitored process `{target}` is now running",
                "no_alerts": "No alerts configured. Use `/alert add` to create one.",
                "configured_alerts": "Configured Alerts",
                "alert_created": "✅ {type} alert '{name}' created",
                "alert_removed": "Removed alert `{name}`",
                "alert_not_found": "Alert not found",
                "channel_set": "Default alert channel set to {channel}",
                "path_invalid": "Path `{path}` is not a valid directory"
            },
            "management": {
                "module_reloaded": "✅ Module Reloaded",
                "reload_success": "Successfully reloaded `{module}`",
                "reload_failed": "❌ Reload Failed",
                "reload_error": "Failed to reload `{module}`",
                "commands_synced": "✅ Commands Synced",
                "sync_success": "Successfully synced {count} commands",
                "sync_failed": "❌ Sync Failed",
                "bot_status": "🤖 Bot Status",
                "bot_info": "Bot Information",
                "system_resources": "System Resources",
                "loaded_modules": "Loaded Modules",
                "configuration": "Configuration",
                "recent_logs": "📋 Recent Logs",
                "restarting": "🔄 Restarting Bot",
                "restart_attempt": "Attempting to restart bot service...",
                "restart_failed": "❌ Restart Failed",
                "not_systemd": "Bot is not running as a systemd service. Manual restart required.",
                "shutting_down": "🛑 Shutting Down",
                "shutdown_message": "Bot is shutting down gracefully...",
                "code_executed": "✅ Code Executed",
                "execution_error": "❌ Execution Error",
                "owner_only": "❌ Only the bot owner can use management commands.",
                "bulk_reload": "🔄 Bulk Reload Results"
            },
            "config": {
                "update_interval_set": "Update interval set to {interval} seconds",
                "invalid_interval": "Invalid interval. Must be between 5 and 300 seconds.",
                "disk_added": "Added disk `{path}` to monitoring list",
                "disk_removed": "Removed disk `{path}` from monitoring list",
                "disk_not_monitored": "Disk `{path}` is not being monitored",
                "current_config": "Current Configuration",
                "config_reset": "Configuration reset to defaults",
                "config_exported": "Configuration exported successfully",
                "export_failed": "Failed to export configuration"
            },
            "docker": {
                "containers": "Docker Containers",
                "no_containers": "No Docker containers found",
                "container_started": "✅ Container `{name}` started successfully",
                "container_stopped": "🛑 Container `{name}` stopped successfully",
                "container_restarted": "🔄 Container `{name}` restarted successfully",
                "operation_failed": "❌ Operation failed",
                "docker_unavailable": "Docker is not available or accessible",
                "container_not_found": "Container not found"
            },
            "common": {
                "error": "Error",
                "success": "Success",
                "failed": "Failed",
                "loading": "Loading...",
                "none": "None",
                "enabled": "Enabled",
                "disabled": "Disabled",
                "running": "Running",
                "stopped": "Stopped",
                "yes": "Yes",
                "no": "No"
            }
        }

        # Save default English file
        self.save_language('en', default_translations)
        self.languages['en'] = default_translations

    def save_language(self, lang_code: str, translations: Dict[str, Any]):
        """Save language translations to file"""
        file_path = os.path.join(self.languages_dir, f"{lang_code}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved language file: {lang_code}")
        except IOError as e:
            self.logger.error(f"Failed to save language file {lang_code}: {e}")

    def get_available_languages(self) -> list:
        """Get list of available language codes"""
        return list(self.languages.keys())

    def get_text(self, key: str, lang: str = None, **kwargs) -> str:
        """
        Get translated text for a given key

        Args:
            key: Translation key in format "category.key"
            lang: Language code (defaults to default_language)
            **kwargs: Format parameters for the text

        Returns:
            Translated and formatted text
        """
        if lang is None:
            lang = self.default_language

        # Fallback to default language if requested language not available
        if lang not in self.languages:
            lang = self.default_language

        # Split key into category and subkey
        try:
            category, subkey = key.split('.', 1)
        except ValueError:
            self.logger.warning(f"Invalid translation key format: {key}")
            return key

        # Get translation
        language_data = self.languages.get(lang, {})
        category_data = language_data.get(category, {})
        text = category_data.get(subkey, key)

        # Format with provided parameters
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError) as e:
            self.logger.warning(f"Failed to format translation '{key}': {e}")
            return text

    def t(self, key: str, lang: str = None, **kwargs) -> str:
        """Shorthand for get_text"""
        return self.get_text(key, lang, **kwargs)

# Global instance
i18n = I18nManager()
