class Account:
    """An account has a balance and a holder.
    一个账户拥有余额和持有人。

    >>> a = Account('John')
    >>> a.deposit(10)
    10
    >>> a.balance
    10
    >>> a.interest
    0.02
    >>> a.time_to_retire(10.25)  # 10 -> 10.2 -> 10.404（每年按利息增长）
    2
    >>> a.balance                # Calling time_to_retire method should not change the balance / 调用 time_to_retire 方法不应改变余额
    10
    >>> a.time_to_retire(11)     # 10 -> 10.2 -> ... -> 11.040808032（需要 5 年）
    5
    >>> a.time_to_retire(100)
    117
    """
    max_withdrawal = 10
    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        if amount > self.max_withdrawal:
            return "Can't withdraw that amount"
        self.balance = self.balance - amount
        return self.balance

    def time_to_retire(self, amount):
        """Return the number of years until balance would grow to amount.
        返回余额增长到 amount 所需的年数。
        """
        assert self.balance > 0 and amount > 0 and self.interest > 0
        n = 0
        new_balance = self.balance
        while new_balance < amount:
            new_balance = new_balance * (1 + self.interest)
            n += 1
        return n


class FreeChecking(Account):
    """A bank account that charges for withdrawals, but the first two are free!
    一种取款要收费的银行账户，但前两次取款是免费的！

    >>> ch = FreeChecking('Jack')
    >>> ch.balance = 20
    >>> ch.withdraw(100)  # First one's free. Still counts as a free withdrawal even though it was unsuccessful / 第一次免费。即使取款失败，也算作一次免费取款
    'Insufficient funds'
    >>> ch.withdraw(3)    # Second withdrawal is also free / 第二次取款同样免费
    17
    >>> ch.balance
    17
    >>> ch.withdraw(3)    # Now there is a fee because free_withdrawals is only 2 / 现在要收手续费了，因为 free_withdrawals 只有 2 次
    13
    >>> ch.withdraw(3)
    9
    >>> ch2 = FreeChecking('John')
    >>> ch2.balance = 10
    >>> ch2.withdraw(3) # No fee / 不收手续费
    7
    >>> ch.withdraw(3)  # ch still charges a fee / ch 仍然收手续费
    5
    >>> ch.withdraw(5)  # Not enough to cover fee + withdraw / 余额不足以支付手续费 + 取款金额
    'Insufficient funds'
    """
    withdraw_fee = 1
    free_withdrawals = 2

    "*** YOUR CODE HERE ***"


def without(s, i):
    """Return a new linked list like s but without the element at index i.
    返回一个与 s 相同但去掉了索引 i 处元素的新链表。

    >>> s = Link(3, Link(5, Link(7, Link(9))))
    >>> without(s, 0)
    Link(5, Link(7, Link(9)))
    >>> without(s, 2)
    Link(3, Link(5, Link(9)))
    >>> without(s, 4)           # There is no index 4, so all of s is retained. / 不存在索引 4，因此 s 的全部元素都保留
    Link(3, Link(5, Link(7, Link(9))))
    >>> without(s, 4) is not s  # Make sure a copy is created / 确保创建的是一个副本
    True
    """
    if s == Link.empty:
        return Link.empty

    if s.rest != Link.empty:
        if i < 0:
            return Link(s.first, without(s.rest, -1))
        if i == 0:
            return Link(s.rest.first, without(s.rest.rest, -1))
        if i > 0:
            return Link(s.first, without(s.rest, i - 1))
    else:
        return Link(s.first)


def duplicate_link(s, val):
    """Mutates s so that each element equal to val is followed by another val.
    修改 s，使得每个等于 val 的元素后面都紧跟着另一个 val。

    >>> x = Link(5, Link(4, Link(5)))
    >>> duplicate_link(x, 5)
    >>> x
    Link(5, Link(5, Link(4, Link(5, Link(5)))))
    >>> y = Link(2, Link(4, Link(6, Link(8))))
    >>> duplicate_link(y, 10)
    >>> y
    Link(2, Link(4, Link(6, Link(8))))
    >>> z = Link(1, Link(2, (Link(2, Link(3)))))
    >>> duplicate_link(z, 2) # ensures that back to back links with val are both duplicated / 确保连续相邻的 val 节点都被复制
    >>> z
    Link(1, Link(2, Link(2, Link(2, Link(2, Link(3))))))
    """
    if s == Link.empty:
        return
    while s != Link.empty:
        if s.first == val:
            tmp = s.rest
            s.rest = Link(val, tmp)
            s = tmp
        else:
            s = s.rest


class Link:
    """A linked list.
    一个链表。

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s) / 显示 repr(s) 的内容
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s) / 打印 str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

