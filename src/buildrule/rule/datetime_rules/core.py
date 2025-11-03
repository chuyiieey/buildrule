# src/rule_engine/datetime_rules/core.py
from datetime import datetime, date, timedelta
from ...rule_node import RuleNode


class DateAfterRule(RuleNode[datetime]):
    type_name = "DATE_AFTER"

    def __init__(self, target_date: datetime):
        self.target_date = target_date

    def evaluate(self, condition: datetime) -> bool:
        return condition > self.target_date


class DateBeforeRule(RuleNode[datetime]):
    type_name = "DATE_BEFORE"

    def __init__(self, target_date: datetime):
        self.target_date = target_date

    def evaluate(self, condition: datetime) -> bool:
        return condition < self.target_date


class DateInRangeRule(RuleNode[datetime]):
    type_name = "DATE_IN_RANGE"

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def evaluate(self, condition: datetime) -> bool:
        return self.start_date <= condition <= self.end_date


class DateTodayRule(RuleNode[date]):
    type_name = "DATE_IS_TODAY"

    def __init__(self):
        pass

    def evaluate(self, condition: date) -> bool:
        return condition == datetime.now().date()


class DateWithinDaysRule(RuleNode[datetime]):
    type_name = "DATE_WITHIN_DAYS"

    def __init__(self, days_before: int, days_after: int):
        self.days_before = days_before
        self.days_after = days_after

    def evaluate(self, condition: datetime) -> bool:
        now = datetime.now()
        start = now - timedelta(days=self.days_before)
        end = now + timedelta(days=self.days_after)
        return start <= condition <= end
