class BalanceDescriptor:
    """Дескриптор для контролю доступу до балансу."""
    def __init__(self):
        self._value = 0

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        raise AttributeError("Зміна балансу напряму заборонена. Використовуйте методи класу.")

    def set_value(self, instance, value):
        if value < 0:
            raise ValueError("Баланс не може бути від'ємним.")
        self._value = value


class Account:
    """Клас для моделювання рахунку з контролем доступу до балансу."""
    balance = BalanceDescriptor()  # Дескриптор для властивості баланс

    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")
        self.balance.set_value(self, initial_balance)

    def __setattr__(self, key, value):
        if key == 'balance':
            raise AttributeError("Зміна балансу через setattr заборонена. Використовуйте методи класу.")
        super().__setattr__(key, value)

    def __getattr__(self, item):
        return f"Властивість '{item}' не існує."

    @property
    def balance(self):
        return self.__class__.balance.__get__(self, Account)

    def deposit(self, amount):
        """Метод для поповнення рахунку."""
        if amount <= 0:
            raise ValueError("Сума поповнення має бути додатною.")
        self.balance.set_value(self, self.balance + amount)

    def withdraw(self, amount):
        """Метод для зняття коштів з рахунку."""
        if amount <= 0:
            raise ValueError("Сума зняття має бути додатною.")
        if self.balance < amount:
            raise ValueError("Недостатньо коштів на рахунку.")
        self.balance.set_value(self, self.balance - amount)


# Приклад використання:
account = Account(100)  # Створюємо рахунок з початковим балансом 100
print(account.balance)  # Виводимо баланс

account.deposit(50)  # Поповнюємо рахунок на 50
print(account.balance)  # Виводимо баланс

try:
    account.balance = 200  # Спроба змінити баланс напряму
except AttributeError as e:
    print(e)

try:
    print(account.some_nonexistent_property)  # Доступ до неіснуючої властивості
except AttributeError as e:
    print(e)
