'''python
''''
Thank you very much for your review.
I highly appreciate the hard work you do.

I don't see a way to remove parenthesis in line 121
since it contains a two rows expression.

The comment about add_record in CashCalculator.
The problem statement clearly says:

Калькулятор денег должен уметь:

 1.  Сохранять новую запись о расходах методом add_record()

Russian is not my primary language so I understood that I must
set this method inside the CashCakculator

Thank you for your brilliant explanations
'''
''''

import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record():
    "Createsa list of a new uploaded data."

    def __init__(self, amount, comment=None, date=None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = self.date2day(date)

    def date2day(self, day):
        "Converting str(date) into date format"

        if day:
            return dt.datetime.strptime(day, DATE_FORMAT).date()

        return dt.datetime.now().date()


class Calculator:
    '''
    Calculates the remanings based on daily limit
    and returns recommendations if there is a room
    for additional spending (cash calculation) or
    for another meal (in calories case)
    '''

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record):
        "Adding record to calories burning history."

        self.records.append(record)

    def today(self):
        "Returns today's date"

        self.now = dt.datetime.now().date()
        return self.now

    def total_today_spendings(self):
        "Calculates daily spendings."

        now = self.today()
        return sum(spent.amount for spent
                   in self.records
                   if spent.date == now)

    def get_week_stats(self):
        "Calculates amount spent for last seven days."

        week = self.today() - dt.timedelta(days=7)
        return sum(spent.amount for spent in self.records
                   if (spent.date >= week
                       and spent.date <= self.today()))

    def get_today_stats(self):
        "Returns todays' spendings."

        return self.total_today_spendings()

    def remain(self):
        return (self.limit - self.get_today_stats())


class CaloriesCalculator(Calculator):
    "Calculates remained calories."

    def __init__(self, limit) -> None:
        super().__init__(limit)

    def get_calories_remained(self):
        "Summing all blown calories and returns recommendation."

        remained = super().remain()
        if remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    '''
    Calculates remained cash based on daily limit.
    Result is returned in rubles with on-flight conversion
    from EURO and USD.
    Requires currency parameter.
    '''

    USD_RATE = 60.
    EURO_RATE = 70.
    RUB_RATE = 1.

    def __init__(self, limit) -> None:
        super().__init__(limit)
        self.currency_dict = {'usd': (self.USD_RATE, 'USD'),
                              'eur': (self.EURO_RATE, 'Euro'),
                              'rub': (self.RUB_RATE, 'руб')}

    def get_today_cash_remained(self, currency):
        "Calculates remaining cash to spend today."

        currency_keys = ('", "').join(self.currency_dict)

        if currency not in self.currency_dict:
            raise ValueError(f'Available options are: "{currency_keys}"')

        else:
            remained = (super().remain()
                        / self.currency_dict[currency][0])

            if remained == 0:
                return 'Денег нет, держись'

            if remained > 0:
                return (f'На сегодня осталось {remained:.2f} '
                        f'{self.currency_dict[currency][1]}')
            return ('Денег нет, держись: твой долг - '
                    f'{-1*remained:.2f} {self.currency_dict[currency][1]}')
