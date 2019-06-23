from enum import Enum


class WaterDrinkingReminderConversationState(Enum):
    START = 1,
    ASK_HYDRATION_HABIT = 2,
    ASK_WAKEUP_TIME = 3,
    ASK_BED_TIME = 4,
    SLEEP = 5,
    ASK_FINISH_DRINKING = 6,
