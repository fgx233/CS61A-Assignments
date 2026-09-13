passphrase = 'REPLACE_THIS_WITH_PASSPHRASE'

def midsem_survey(p):
    """
    You do not need to understand this code.
    你不需要理解这段代码。

    >>> midsem_survey(passphrase)
    '2bf925d47c03503d3ebe5a6fc12d479b8d12f14c0494b43deba963a0'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


class VendingMachine:
    """A vending machine that vends some product for some price.

    一台自动售货机，按照某个价格售卖某种商品。

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """                                     
    def __init__(self, product, price):
        """Set the product and its price, as well as other instance attributes.

        设置商品及其价格，以及其他实例属性。
        """
        self.product = product
        self.price = price
        self.stocks = 0
        self.balance = 0


    def restock(self, n):
        """Add n to the stock and return a message about the updated stock level.

        E.g., Current candy stock: 3

        把 n 加到库存中，并返回一条关于更新后库存量的消息。

        例如：Current candy stock: 3
        """
        self.stocks += n
        msg = f'Current {self.product} stock: {self.stocks}'
        return msg

    def add_funds(self, n):
        """If the machine is out of stock, return a message informing the user to restock
        (and return their n dollars).

        E.g., Nothing left to vend. Please restock. Here is your $4.

        Otherwise, add n to the balance and return a message about the updated balance.

        E.g., Current balance: $4

        如果售货机已经没有库存，返回一条消息提示用户补货（并把他们的 n 元退还）。

        例如：Nothing left to vend. Please restock. Here is your $4.

        否则，把 n 加到余额中，并返回一条关于更新后余额的消息。

        例如：Current balance: $4
        """
        if self.stocks == 0:
            msg = f'Nothing left to vend. Please restock. Here is your ${n}.'
        else:
            self.balance += n
            msg = f'Current balance: ${self.balance}'
        return msg

    def vend(self):
        """Dispense the product if there is sufficient stock and funds and
        return a message. Update the stock and balance accordingly.

        E.g., Here is your candy and $2 change.

        If not, return a message suggesting how to correct the problem.

        E.g., Nothing left to vend. Please restock.
              Please add $3 more funds.

        如果库存和余额都足够，就把商品发放出去并返回一条消息，
        同时相应地更新库存和余额。

        例如：Here is your candy and $2 change.

        如果不满足条件，则返回一条消息，提示如何解决这个问题。

        例如：Nothing left to vend. Please restock.
              Please add $3 more funds.
        """
        if self.stocks >= 1 and self.price <= self.balance:
            self.stocks -= 1
            if self.balance == self.price:
                self.balance = 0
                msg = f'Here is your {self.product}.'
            else:
                msg = f'Here is your {self.product} and ${self.balance - self.price} change.'
                self.balance = 0
        elif self.stocks >= 1 and self.price > self.balance:
            msg = f'Please add ${self.price - self.balance} more funds.'
        elif self.stocks == 0:
            msg = f'Nothing left to vend. Please restock.'
        return msg


def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    把正整数 n 的各个数字按顺序存进一个链表中。

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> store_digits(2450)
    Link(2, Link(4, Link(5, Link(0))))
    >>> store_digits(20105)
    Link(2, Link(0, Link(1, Link(0, Link(5)))))
    >>> # a check for restricted functions / 检查是否使用了被禁止的函数
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    """
    result = Link.empty
    while n != 0:
        result = Link(n % 10, result)
        n //= 10
    return result


def deep_map_mut(func, s):
    """Mutates a deep link s by replacing each item found with the
    result of calling func on the item. Does NOT create new Links (so
    no use of Link's constructor).

    Does not return the modified Link object.

    对一个嵌套链表 s 进行原地修改：把其中找到的每个元素替换为对该元素
    调用 func 后的结果。不允许创建新的 Link（即不能使用 Link 的构造函数）。

    不返回修改后的 Link 对象。

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print(link1)
    <3 <4> 5 6>
    >>> # Disallow the use of making new Links before calling deep_map_mut / 在调用 deep_map_mut 前禁止创建新的 Link
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    if type(s) != type(s.first):
        s.first = func(s.first)
    else:
        deep_map_mut(func, s.first)
    if s.rest != Link.empty:
        deep_map_mut(func, s.rest)


def two_list(vals, counts):
    """
    Returns a linked list according to the two lists that were passed in. Assume
    vals and counts are the same size. Elements in vals represent the value, and the
    corresponding element in counts represents the number of this value desired in the
    final linked list. Assume all elements in counts are greater than 0. Assume both
    lists have at least one element.

    根据传入的两个列表返回一个链表。假设 vals 和 counts 的长度相同。
    vals 中的元素代表值，counts 中对应位置的元素代表该值在最终链表中
    需要出现的次数。假设 counts 中的所有元素都大于 0，并且两个列表
    都至少有一个元素。

    >>> a = [1, 3]
    >>> b = [1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
    """
    result = Link.empty
    i = len(vals) - 1
    while i >= 0:
        j = counts[i] - 1
        while j >= 0:
            result = Link(vals[i], result)
            j -= 1
        i -= 1
    return result


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

