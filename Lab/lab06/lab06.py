class Transaction:
    def __init__(self, id, before, after):
        self.id = id
        self.before = before
        self.after = after

    def changed(self):
        """Return whether the transaction resulted in a changed balance.
        返回该交易是否导致余额发生了变化。
        """
        if self.before != self.after:
            return True
        return False

    def report(self):
        """Return a string describing the transaction.
        返回一个描述该交易的字符串。

        >>> Transaction(3, 20, 10).report()
        '3: decreased 20->10'
        >>> Transaction(4, 20, 50).report()
        '4: increased 20->50'
        >>> Transaction(5, 50, 50).report()
        '5: no change'
        """
        msg = 'no change'
        if self.changed():
            if self.before > self.after:
                msg = "decreased " + str(self.before) + "->" + str(self.after)
            else:
                msg = "increased " + str(self.before) + "->" + str(self.after)
        return str(self.id) + ': ' + msg

class BankAccount:
    """A bank account that tracks its transaction history.
    一个会记录自身交易历史的银行账户。

    >>> a = BankAccount('Eric')
    >>> a.deposit(100)    # Transaction 0 for a  # a 的第 0 笔交易
    100
    >>> b = BankAccount('Erica')
    >>> a.withdraw(30)    # Transaction 1 for a  # a 的第 1 笔交易
    70
    >>> a.deposit(10)     # Transaction 2 for a  # a 的第 2 笔交易
    80
    >>> b.deposit(50)     # Transaction 0 for b  # b 的第 0 笔交易
    50
    >>> b.withdraw(10)    # Transaction 1 for b  # b 的第 1 笔交易
    40
    >>> a.withdraw(100)   # Transaction 3 for a  # a 的第 3 笔交易
    'Insufficient funds'
    >>> len(a.transactions)
    4
    >>> len([t for t in a.transactions if t.changed()])
    3
    >>> for t in a.transactions:
    ...     print(t.report())
    0: increased 0->100
    1: decreased 100->70
    2: increased 70->80
    3: no change
    >>> b.withdraw(100)   # Transaction 2 for b  # b 的第 2 笔交易
    'Insufficient funds'
    >>> b.withdraw(30)    # Transaction 3 for b  # b 的第 3 笔交易
    10
    >>> for t in b.transactions:
    ...     print(t.report())
    0: increased 0->50
    1: decreased 50->40
    2: no change
    3: decreased 40->10
    """

    # *** YOU NEED TO MAKE CHANGES IN SEVERAL PLACES IN THIS CLASS ***
    # *** 你需要在这个类的多个地方进行修改 ***

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
        self.transactions_times = 0
        self.transactions = []

    def deposit(self, amount):
        """Increase the account balance by amount, add the deposit
        to the transaction history, and return the new balance.
        将账户余额增加 amount，把这笔存款加入交易历史，并返回新的余额。
        """
        before = self.balance
        self.balance = self.balance + amount
        after = self.balance
        self.transactions.append(Transaction(self.transactions_times, before, after))
        self.transactions_times += 1
        return self.balance

    def withdraw(self, amount):
        """Decrease the account balance by amount, add the withdraw
        to the transaction history, and return the new balance.
        将账户余额减少 amount，把这笔取款加入交易历史，并返回新的余额。
        """
        before = self.balance
        after = self.balance
        if amount > self.balance:
            self.transactions.append(Transaction(self.transactions_times, before, after))
            self.transactions_times += 1
            return 'Insufficient funds'
        self.balance = self.balance - amount
        after = self.balance
        self.transactions.append(Transaction(self.transactions_times, before, after))
        self.transactions_times += 1
        return self.balance


class Email:
    """An email has the following instance attributes:
    一封邮件具有以下实例属性：

        msg (str): the contents of the message
                   邮件的内容
        sender (Client): the client that sent the email
                         发送这封邮件的客户端
        recipient_name (str): the name of the recipient (another client)
                              收件人（另一个客户端）的名字
    """
    def __init__(self, msg, sender, recipient_name):
        self.msg = msg
        self.sender = sender
        self.recipient_name = recipient_name

class Server:
    """Each Server has one instance attribute called clients that is a
    dictionary from client names to client objects.
    每个 Server 都有一个名为 clients 的实例属性，它是一个从客户端名字
    映射到客户端对象的字典。
    """
    def __init__(self):
        self.clients = {}

    def send(self, email):
        """Append the email to the inbox of the client it is addressed to.
            email is an instance of the Email class.
        把这封邮件追加到它所寄往的客户端的收件箱中。
            email 是 Email 类的一个实例。
        """
        self.clients[email.recipient_name].inbox.append(email)

    def register_client(self, client):
        """Add a client to the clients mapping (which is a 
        dictionary from client names to client instances).
            client is an instance of the Client class.
        把一个客户端加入 clients 映射中（它是一个从客户端名字
        映射到客户端实例的字典）。
            client 是 Client 类的一个实例。
        """
        self.clients[client.name] = client

class Client:
    """A client has a server, a name (str), and an inbox (list).
    一个客户端拥有一个服务器、一个名字（str）和一个收件箱（list）。

    >>> s = Server()
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> a.compose('Hello, World!', 'Bob')
    >>> b.inbox[0].msg
    'Hello, World!'
    >>> a.compose('CS 61A Rocks!', 'Bob')
    >>> len(b.inbox)
    2
    >>> b.inbox[1].msg
    'CS 61A Rocks!'
    >>> b.inbox[1].sender.name
    'Alice'
    """
    def __init__(self, server, name):
        self.inbox = []
        self.server = server
        self.name = name
        server.register_client(self)

    def compose(self, message, recipient_name):
        """Send an email with the given message to the recipient.
        将包含给定消息的邮件发送给收件人。
        """
        email = Email(message, self, recipient_name)
        self.server.send(email)


class Mint:
    """A mint creates coins by stamping on years.
    造币厂通过在硬币上印上年份来铸造硬币。

    The update method sets the mint's stamp to Mint.present_year.
    update 方法会把造币厂的印章（年份）设置为 Mint.present_year。

    >>> mint = Mint()
    >>> mint.year
    2024
    >>> dime = mint.create(Dime)
    >>> dime.year
    2024
    >>> Mint.present_year = 2104  # Time passes  # 时间流逝
    >>> nickel = mint.create(Nickel)
    >>> nickel.year     # The mint has not updated its stamp yet  # 造币厂还没有更新它的印章
    2024
    >>> nickel.worth()  # 5 cents + (80 - 50 years)  # 5 美分 + (80 - 50 年)
    35
    >>> mint.update()   # The mint's year is updated to 2104  # 造币厂的年份被更新为 2104
    >>> Mint.present_year = 2179     # More time passes  # 更多时间流逝
    >>> mint.create(Dime).worth()    # 10 cents + (75 - 50 years)  # 10 美分 + (75 - 50 年)
    35
    >>> Mint().create(Dime).worth()  # A new mint has the current year  # 新的造币厂使用当前年份
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)  # 10 美分 + (155 - 50 年)
    115
    >>> Dime.cents = 20  # Upgrade all dimes!  # 升级所有的 dime！
    >>> dime.worth()     # 20 cents + (155 - 50 years)  # 20 美分 + (155 - 50 年)
    125
    """
    present_year = 2024

    def __init__(self):
        self.year = Mint.present_year
        self.update()

    def create(self, coin):
        return coin(self.year)

    def update(self):
        self.year = Mint.present_year

class Coin:
    cents = None # will be provided by subclasses, but not by Coin itself
                 # 由子类提供，Coin 本身不提供

    def __init__(self, year):
        self.year = year

    def worth(self):
        inc = (Mint.present_year - self.year) if (Mint.present_year - self.year )>= 50 else 50
        return self.cents + inc - 50

class Nickel(Coin):
    cents = 5

class Dime(Coin):
    cents = 10
