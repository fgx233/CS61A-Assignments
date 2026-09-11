"""CS 61A presents Ants Vs. SomeBees.

CS 61A 出品：《蚂蚁大战蜜蜂》。
"""

import random
from ucb import main, interact, trace
from collections import OrderedDict

#######################
# Core Classes 核心类 #
#######################


class Place:
    """A Place holds insects and has an exit to another Place.

    Place（地点）容纳昆虫，并有一个通往另一个 Place 的出口。
    """
    is_hive = False  # Whether this Place is the Hive 该地点是否是蜂巢

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).

        用给定的 NAME 和 EXIT 创建一个 Place。

        name -- 一个字符串；这个 Place 的名字。
        exit -- 从这个 Place 出去后到达的 Place（可以为 None）。
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees 一个存放 Bee 的列表
        self.ant = None       # An Ant 一只 Ant
        self.entrance = None  # A Place 一个 Place（入口）
        # Phase 1: Add an entrance to the exit
        # 阶段 1：给出口（exit）设置入口（entrance）
        # BEGIN Problem 2
        if exit != None:
            exit.entrance = self
        # END Problem 2

    def add_insect(self, insect):
        """Asks the insect to add itself to this place. This method exists so
        that it can be overridden in subclasses.

        请求这只昆虫把自己加入本地点。之所以单独写成一个方法，是为了能在子类中被重写。
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """Asks the insect to remove itself from this place. This method exists so
        that it can be overridden in subclasses.

        请求这只昆虫把自己从本地点移除。之所以单独写成一个方法，是为了能在子类中被重写。
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place.

    Insect（昆虫）是 Ant 和 Bee 的基类，拥有生命值（health）和所在地点（Place）。
    """

    next_id = 0  # Every insect gets a unique id number 每只昆虫都会分到一个唯一的编号
    damage = 0   # Damage dealt per attack 每次攻击造成的伤害
    # ADD CLASS ATTRIBUTES HERE
    # 在此添加类属性
    is_waterproof = False

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE.

        创建一只昆虫，指定其生命值 health 和初始地点 PLACE。
        """
        self.health = health
        self.place = place

        # assign a unique ID to every insect
        # 给每只昆虫分配一个唯一的 ID
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining.

        将生命值减少 AMOUNT；如果生命值已耗尽，就把这只昆虫从它所在的地点移除。

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.zero_health_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn.

        每一回合执行的动作。
        """

    def zero_health_callback(self):
        """Called when health reaches 0 or below.

        当生命值降到 0 或以下时被调用。
        """
        if self.name == 'Queen':
            raise AntsLoseException()

    def add_to(self, place):
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony.

    Ant（蚂蚁）占据一个地点，并为蚁群工作。
    """

    implemented = False  # Only implemented Ant classes should be instantiated
                         # 只有已实现（implemented）的 Ant 子类才应该被实例化
    food_cost = 0        # Food required to deploy this ant 部署这只蚂蚁所需的食物
    is_container = False # Whether this ant can hold another ant 这只蚂蚁能否容纳另一只蚂蚁
    # ADD CLASS ATTRIBUTES HERE
    # 在此添加类属性

    def __init__(self, health=1):
        super().__init__(health)
        self.doubled = False

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        if place.ant is None:
            place.ant = self
        else:
            # BEGIN Problem 8b
            if place.ant.is_container and place.ant.can_contain(self):
                place.ant.store_ant(self)
            elif self.is_container and self.can_contain(place.ant):
                self.store_ant(place.ant)
                place.ant = self
            else:
                assert place.ant is None, 'Too many ants in {0}'.format(place)
            # END Problem 8b
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """Double this ants's damage, if it has not already been doubled.

        将这只蚂蚁的伤害翻倍（如果之前还没有被翻倍过）。
        """
        # BEGIN Problem 12
        if self.doubled == False:
            self.damage *= 2
            self.doubled = True
            if self.is_container and self.ant_contained != None:
                self.ant_contained.double()
        else:
            if self.is_container and self.ant_contained != None:
                self.ant_contained.double()
        # END Problem 12


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony.

    HarvesterAnt（收割蚁）每回合为蚁群额外生产 1 份食物。
    """

    name = 'Harvester'
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    food_cost = 2

    def action(self, gamestate):
        """Produce 1 additional food for the colony.

        gamestate -- The GameState, used to access game state information.

        为蚁群额外生产 1 份食物。

        gamestate -- GameState 对象，用于访问游戏的状态信息。
        """
        # BEGIN Problem 1
        gamestate.food += 1
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range.

    ThrowerAnt（投掷蚁）每回合向射程内最近的一只 Bee 投掷一片叶子。
    """

    name = 'Thrower'
    implemented = True
    damage = 1
    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    # 在此添加/覆盖类属性
    food_cost = 3
    lower_bound = 0
    upper_bound = float('inf')

    def nearest_bee(self):
        """Return the nearest Bee in a Place (that is not the hive) connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).

        沿着 entrance 一路向前查找，返回与本 ThrowerAnt 所在 Place 相连的某个
        Place（不含蜂巢 Hive）中最近的那只 Bee。

        如果不存在这样的 Bee（或射程内没有 Bee），则返回 None。
        """
        # BEGIN Problem 3 and 4
        pos = self.place
        i = 0
        while i < self.lower_bound:
            if pos.entrance != None:
                pos = pos.entrance
                i += 1
            else:
                return None
        while not pos.is_hive and i <= self.upper_bound:
            if pos.bees != []:
                    return random_bee(pos.bees)
            pos = pos.entrance
            i += 1
        return None
            
        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its health.

        向目标 Bee 投掷一片叶子，减少它的生命值。
        """
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range.

        向射程内最近的一只 Bee 投掷叶子。
        """
        self.throw_at(self.nearest_bee())


def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty.

    从一个 bee 列表中随机返回一只蜜蜂；如果列表为空，则返回 None。
    """
    assert isinstance(bees, list), \
        "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

####################
# Extensions 扩展 #
####################


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away.

    一种 ThrowerAnt，只向距离不超过 3 个地点的 Bee 投掷叶子。
    """

    name = 'Short'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    upper_bound = 3
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem 4


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away.

    一种 ThrowerAnt，只向距离至少 5 个地点的 Bee 投掷叶子。
    """

    name = 'Long'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    lower_bound = 5
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem 4


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires.

    FireAnt（火蚁）阵亡时会烧灼它所在地点的所有 Bee。
    """

    name = 'Fire'
    damage = 3
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    # BEGIN Problem 5
    implemented = True   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem 5

    def __init__(self, health=3):
        """Create an Ant with a HEALTH quantity.

        创建一只生命值为 HEALTH 的蚂蚁。
        """
        super().__init__(health)

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.

        将生命值减少 AMOUNT；如果生命值已耗尽，就把这只 FireAnt 从它所在的地点移除。

        注意要减少当前地点每一只蜜蜂的生命值；如果这只火蚁阵亡，还要追加额外伤害。
        """
        # BEGIN Problem 5
        total_damage = self.damage + amount if self.health <= amount else amount
        for i in self.place.bees[:]:
            i.reduce_health(total_damage)
        super().reduce_health(amount)
        # END Problem 5

# BEGIN Problem 6
# The WallAnt class
# WallAnt（墙蚁）类
class WallAnt(Ant):
    name = 'Wall'
    implemented = True
    food_cost = 4
    def __init__(self, health=4):
        super().__init__(health)
# END Problem 6

# BEGIN Problem 7
# The HungryAnt Class
# HungryAnt（饥饿蚁）类
class HungryAnt(Ant):
    name = 'Hungry'
    implemented = True
    food_cost = 4
    chew_cooldown = 3
    def __init__(self, health=1):
        self.cooldown = 0
        super().__init__(health)
    def action(self, gamestate):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        if self.place.bees != []:
            to_be_killed = random_bee(self.place.bees)
            to_be_killed.reduce_health(to_be_killed.health)
            self.cooldown = HungryAnt.chew_cooldown

# END Problem 7


class ContainerAnt(Ant):
    """
    ContainerAnt can share a space with other ants by containing them.

    ContainerAnt（容器蚁）通过“容纳”其他蚂蚁，从而与它们共享同一个格子。
    """
    is_container = True

    def __init__(self, health):
        super().__init__(health)
        self.ant_contained = None

    def can_contain(self, other):
        # BEGIN Problem 8a
        if self.ant_contained == None and other.is_container == False:
            return True
        return False
        # END Problem 8a

    def store_ant(self, ant):
        # BEGIN Problem 8a
        self.ant_contained = ant
        # END Problem 8a

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # Special handling for container ants
        # 针对容器蚁的特殊处理
        if place.ant is self:
            # Container was removed. Contained ant should remain in the game
            # 容器蚁被移除了，被它容纳的那只蚂蚁应该继续留在游戏中
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            # 其余情况按普通行为处理
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN Problem 8a
        if self.ant_contained != None:
            self.ant_contained.action(gamestate)
        # END Problem 8a


class BodyguardAnt(ContainerAnt):
    """BodyguardAnt provides protection to other Ants.

    BodyguardAnt（保镖蚁）为其他蚂蚁提供保护。
    """

    name = 'Bodyguard'
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    # BEGIN Problem 8c
    implemented = True   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    def __init__(self, health=2):
        super().__init__(health)
    # END Problem 8c

# BEGIN Problem 9
# The TankAnt class
# TankAnt（坦克蚁）类
class TankAnt(ContainerAnt):
    name = 'Tank'
    food_cost = 6
    implemented = True
    damage = 1
    def __init__(self, health=2):
        super().__init__(health)
    def action(self, gamestate):
        for bee in self.place.bees[:]:
            bee.reduce_health(self.damage)
        super().action(gamestate)

# END Problem 9


class Water(Place):
    """Water is a place that can only hold waterproof insects.

    Water（水域）是一种只能容纳防水昆虫的地点。
    """

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0.

        向这个地点添加一只昆虫。如果这只昆虫不防水，就把它的生命值降为 0。
        """
        # BEGIN Problem 10
        "*** YOUR CODE HERE ***"
        super().add_insect(insect)

        if insect.is_waterproof == False:
            insect.reduce_health(insect.health)
        # END Problem 10

# BEGIN Problem 11
# The ScubaThrower class
# ScubaThrower（潜水投掷蚁）类
class ScubaThrower(ThrowerAnt):
    food_cost = 6
    is_waterproof = True
    name = 'Scuba'
    implemented = True

# END Problem 11


class QueenAnt(ThrowerAnt):
    """QueenAnt boosts the damage of all ants behind her.

    QueenAnt（蚁后）会提升她身后所有蚂蚁的伤害。
    """

    name = 'Queen'
    food_cost = 7
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    # BEGIN Problem 12
    implemented = True   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem 12

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.

        蚁后会投掷叶子，同时还会把她所在隧道中其他蚂蚁的伤害翻倍。
        """
        # BEGIN Problem 12
        super().action(gamestate)
        pos = self.place.exit
        while pos != None:
            if pos.ant != None:
                pos.ant.double()
            pos = pos.exit
        # END Problem 12

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.

        将生命值减少 AMOUNT；如果蚁后的生命值已耗尽，则发出游戏结束的信号。
        """
        # BEGIN Problem 12
        
        super().reduce_health(amount)
        # END Problem 12


#############################
# Extra Challenge 附加挑战 #
#############################

class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees.

    一种 ThrowerAnt，会让 Bee 陷入减速（Slow）状态。
    """

    name = 'Slow'
    food_cost = 6
    # BEGIN Problem EC 1
    implemented = False   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem EC 1

    def throw_at(self, target):
        # BEGIN Problem EC 1
        "*** YOUR CODE HERE ***"
        # END Problem EC 1


class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing.

    一种 ThrowerAnt，会恐吓 Bee，使它们后退而不是前进。
    """

    name = 'Scary'
    food_cost = 6
    # BEGIN Problem EC 2
    implemented = False   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem EC 2

    def throw_at(self, target):
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place.

    NinjaAnt（忍者蚁）不会阻挡通路，并且会伤害它所在地点的所有蜜蜂。
    """

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    # BEGIN Problem EC 3
    implemented = False   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem EC 3

    def action(self, gamestate):
        # BEGIN Problem EC 3
        "*** YOUR CODE HERE ***"
        # END Problem EC 3


class LaserAnt(ThrowerAnt):
    """ThrowerAnt that damages all Insects standing in its path.

    一种 ThrowerAnt，会伤害挡在它射线路径上的所有昆虫。
    """

    name = 'Laser'
    food_cost = 10
    # OVERRIDE CLASS ATTRIBUTES HERE
    # 在此覆盖类属性
    # BEGIN Problem EC 4
    implemented = False   # Change to True to view in the GUI 改为 True 才能在 GUI 中看到
    # END Problem EC 4

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        # BEGIN Problem EC 4
        return {}
        # END Problem EC 4

    def calculate_damage(self, distance):
        # BEGIN Problem EC 4
        return 0
        # END Problem EC 4

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1


################
# Bees 蜜蜂 #
################

class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants.

    Bee（蜜蜂）沿着出口在各个地点之间移动，并蜇咬蚂蚁。
    """

    name = 'Bee'
    damage = 1
    is_waterproof = True  # Bees can fly over water 蜜蜂能飞过水域


    def sting(self, ant):
        """Attack an ANT, reducing its health by 1.

        攻击一只蚂蚁 ANT，使其生命值减少 1。
        """
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE.

        把这只蜜蜂从当前所在的 Place 移动到新的 PLACE。
        """
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place.

        如果这只蜜蜂无法前进到下一个 Place，则返回 True。
        """
        # Special handling for NinjaAnt
        # 针对 NinjaAnt 的特殊处理
        # BEGIN Problem EC 3
        return self.place.ant is not None
        # END Problem EC 3

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.

        蜜蜂的动作：如果被阻挡，就蜇咬挡住它出口的那只蚂蚁；否则就移动到当前地点的出口。

        gamestate -- GameState 对象，用于访问游戏的状态信息。
        """
        destination = self.place.exit


        if self.blocked():
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        super().add_to( place)

    def remove_from(self, place):
        place.bees.remove(self)
        super().remove_from(place)

    def scare(self, length):
        """
        If this Bee has not been scared before, cause it to attempt to
        go backwards LENGTH times.

        如果这只蜜蜂之前没有被吓到过，就让它尝试后退 LENGTH 次。
        """
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class Wasp(Bee):
    """Class of Bee that has higher damage.

    Wasp（黄蜂）是伤害更高的一类 Bee。
    """
    name = 'Wasp'
    damage = 2


class Boss(Wasp):
    """The leader of the bees. Damage to the boss by any attack is capped.

    Boss（首领）是蜜蜂的头目。任何攻击对它造成的伤害都有上限。
    """
    name = 'Boss'
    damage_cap = 8  # Maximum damage taken from a single attack 单次攻击可造成的最大伤害

    def reduce_health(self, amount):
        super().reduce_health(min(amount, self.damage_cap))


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.

    蜜蜂发起进攻的出发地点（蜂巢）。

    assault_plan -- 一个 AssaultPlan；描述蜜蜂在何时、从何处进入蚁群。
    """
    is_hive = True

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        # 对于 Hive 来说，下面这些属性永远是 None
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)

#############################
# Game Components 游戏组件 #
#############################

class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter

    表示一个蚁群，负责管理全局游戏状态并模拟时间推进。

    属性：
    time -- 已经过去的时间
    food -- 蚁群当前可用的食物总量
    places -- 蚁群中所有地点的列表（包含一个 Hive）
    bee_entrances -- 蜜蜂可以进入的地点列表
    """

    def __init__(self, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.

        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout

        创建一个用于模拟游戏的 GameState。

        参数：
        beehive -- 一个装满蜜蜂的 Hive
        ant_types -- 蚂蚁类的列表
        create_places -- 一个用于创建全部地点的函数
        dimensions -- 一个二元组，表示游戏布局的尺寸
        """
        self.time = 0
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """Configure the places in the colony.

        配置蚁群中的各个地点。
        """
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place,
                      self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self): # Ask ants to take actions 让蚂蚁们执行各自的动作
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees): # Ask bees to take actions 让蜜蜂们执行各自的动作
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0: # Check if player won 检查玩家是否已经获胜
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """Simulate an attack on the ant colony. This is called by the GUI to play the game.

        模拟一次对蚁群的进攻。GUI 通过调用它来进行游戏。
        """
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self) # Bees invade from hive 蜜蜂从蜂巢出发入侵
                yield None # After yielding, players have time to place ants
                           # yield 之后，玩家有时间放置蚂蚁
                self.ants_take_actions()
                self.time += 1
                yield None # After yielding, wait for throw leaf animation to play, then ask bees to take action
                           # yield 之后，等待投掷叶子的动画播放完毕，然后让蜜蜂执行动作
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print('All bees are vanquished. You win!')
            yield True
        except AntsLoseException:
            print('The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.

        在食物足够的前提下放置一只蚂蚁。

        当前的策略（strategy）通过调用这个方法来部署蚂蚁。
        """
        ant_type = self.ant_types[ant_type_name]
        if ant_type.food_cost > self.food:
            print('Not enough food remains to place ' + ant_type.__name__)
        else:
            ant = ant_type()
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game.

        把一只蚂蚁从游戏中移除。
        """
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen normally resides.

    AntHomeBase（蚂蚁大本营）位于隧道尽头，通常是蚁后所在的地方。
    """

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.

        向这个地点添加一只昆虫。

        实际上不能把蚂蚁加入 AntHomeBase。但如果有蜜蜂试图进入 AntHomeBase，
        就会抛出 AntsLoseException，表示游戏结束。
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """Signal that Ants win.

    发出蚂蚁获胜的信号。
    """
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose.

    发出蚂蚁失败的信号。
    """
    raise AntsLoseException()


def ant_types():
    """Return a list of all implemented Ant classes.

    返回所有已实现（implemented）的 Ant 类组成的列表。
    """
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types():
    """Return a list of all implemented Bee classes.

    返回所有已实现的 Bee 类组成的列表。
    """
    all_bee_types = []
    new_types = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """Base game over Exception.

    游戏结束异常的基类。
    """
    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win.

    用于表示蚂蚁获胜的异常。
    """
    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose.

    用于表示蚂蚁失败的异常。
    """
    pass


####################
# Layouts 布局 #
####################


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places.

    注册一批干湿混合的地点（既有水域也有普通隧道）。
    """
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels.

    注册全是干燥隧道的布局。
    """
    wet_layout(queen, register_place, tunnels, length, 0)


###########################
# Assault Plans 进攻计划 #
###########################

class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    蜜蜂进攻蚁群的作战计划。进攻会按预定时刻分成一波波到来。

    AssaultPlan 是一个字典，键是时刻（int），值是波次（Bee 组成的列表）。

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_health, time, count):
        """Add a wave at time with count Bees that have the specified health.

        在 time 时刻添加一个波次，包含 count 只生命值为 bee_health 的蜜蜂。
        """
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees.

        把所有蜜蜂放入蜂巢，并返回这些蜜蜂组成的列表。
        """
        return [bee for wave in self.values() for bee in wave]
