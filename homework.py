
import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record():
    '''Createsa list of a new uploaded data.'''
    
    def __init__(self, amount, comment=None, date=None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = self.date2day(date)
        # self.save()

    def date2day(self, day):
        '''Converting str(date) into date format'''

        if type(day) == str:
            return dt.datetime.strptime(day, DATE_FORMAT).date()
        # elif type(day) != str:
        #     return day    
        else:
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
        self.now = dt.datetime.now().date()
    
    def add_record(self, record):
        '''Adding record to calories burning history.'''

        self.records.append(record)
        return self.records

    def get_conversion_rate(self, currency):
        '''Returns conversion rate based on the currency'''

        if currency == 'eur':
            conversion = self.EURO_RATE
        elif currency == 'usd':
            conversion = self.USD_RATE
        elif currency == 'rub':
            conversion = self.RUB_RATE
        else:
            return (
                'Please check the currency input '
                'Available options are: "rub", "usd" or "eur"')
        return conversion

    def total_today_spendings(self):
        '''Calculates daily cash spendings.'''

        sum = 0
        for i, spent in enumerate(self.records):
            if self.records[i].date == self.now:
                sum += self.records[i].amount
        return sum

    def total_week_spendings(self):
        '''Calculates weekly cash spendings.'''

        sum = 0
        for i, spent in enumerate(self.records):
            if (self.records[i].date >= self.now - dt.timedelta(days=7)
                    and self.records[i].date <= self.now):
                sum += self.records[i].amount
        return sum

    def get_week_stats(self, currency=None):
        '''Calculates amount spent for last seven days.'''

        if currency:
            conversion_rate = self.get_conversion_rate(currency)

            if isinstance(conversion_rate, str):
                return conversion_rate

            else:
                return (
                    'Weekly cash spendings are '
                    f'{self.total_week_spendings(self.records):.2f}')
                   
        return self.total_week_spendings()

    def get_today_stats(self, currency=None):
        '''Returns todays' spendings.'''
      
        if currency:
            conversion_rate = self.get_conversion_rate(currency)
            return self.total_today_spendings() / conversion_rate

        else:
            return self.total_today_spendings()


class CaloriesCalculator(Calculator):
    '''Calculates remained calories.'''

    def __init__(self, limit) -> None:
        super().__init__(limit)
        self.records = []

    def get_calories_remained(self):
        remained = (self.limit -
                    self.get_today_stats())                            
        if remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё,'  
                    f' но с общей калорийностью не более {remained} кКал')
        else:
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
        self.records = []
        self.currency_dict = {'usd': 'USD',
                              'eur': 'Euro',
                              'rub': 'руб'}

    def add_record(self, record):
        '''
        I have no idea why it's here - code can run without it
        but test fails
        '''

        self.records = super().add_record(record)
        return self.records
    
    def get_today_cash_remained(self, currency):
        '''Calculates remaining cash to spend today.'''

        if isinstance(super().get_conversion_rate(currency), str):
            return super().get_conversion_rate(currency)
        else:
            remained = ((self.limit -
                         self.total_today_spendings())
                        / super().get_conversion_rate(currency))

            if remained > 0:
                return (f'На сегодня осталось {remained:.2f} '
                        f'{self.currency_dict[currency]}')
            elif remained == 0:  
                return 'Денег нет, держись'
            else:
                return ('Денег нет, держись: твой долг - '
                        f'{-1*remained:.2f} {self.currency_dict[currency]}')

        return super().get_today_stats(currency)

    def get_week_cash_remained(self, currency):
        '''Calculates spendings within last seven days.'''

        return super().get_week_stats(currency) 
