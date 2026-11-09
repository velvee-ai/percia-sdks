from enum import Enum


class UpdateIntegrationResponse200Service(str, Enum):
    DISCORD = "discord"
    HOME_ASSISTANT = "home_assistant"
    IFTTT = "ifttt"
    PAGERDUTY = "pagerduty"
    SLACK = "slack"
    TEAMS = "teams"
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
