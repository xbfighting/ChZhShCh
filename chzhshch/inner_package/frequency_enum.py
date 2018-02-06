from enum import Enum, unique

@unique
class Frequency(Enum):
    one_min = '1min',
    five_min = '5min',
    fifteen_min = '15min',
    thirty_min = '30min',
    sixty_min = '60min',
    one_day = 'D',
    ween = 'W',
    one_month = 'M',
