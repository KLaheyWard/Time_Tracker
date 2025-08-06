from enum import Enum

from common.constants.cycles import NUM_DAYS_IN_CYCLE, NUM_HOURS_IN_CYCLE

DEFAULT_UNPAID_BREAK_MINUTES = 30
HOURS_PER_DAY_HOLIDAY = 7.5


class DayTypeHoursEnum(Enum):
    REGULAR = round(NUM_HOURS_IN_CYCLE / NUM_DAYS_IN_CYCLE, 30)
    HOLIDAY = HOURS_PER_DAY_HOLIDAY
