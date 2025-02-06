class account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance 

    def deposit(self, money):
        self.balance = self.balance + money 
        print(f'transfer completed, the new balance is: {self.balance}')

    def withdraw(self, money):
        
        if self.balance < money:
            print('not enough money :(')
        else:
            self.balance = self.balance - money
            print(f'transaction completed, the new balance is:  {self.balance}')
        

acc = account('Danil', 1000000)
print(acc.deposit(2000))
print(acc.withdraw(99999))