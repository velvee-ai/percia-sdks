from enum import Enum


class ConnectionService(str, Enum):
    DISCORD = "discord"
    HOME_ASSISTANT = "home_assistant"
    IFTTT = "ifttt"
    PAGERDUTY = "pagerduty"
    SLACK = "slack"
    SMS = "sms"
    TEAMS = "teams"
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"
    WHATSAPP = "whatsapp"

    def __str__(self) -> str:
        return str(self.value)
