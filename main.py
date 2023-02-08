"""
idea:
- start with set amount of money spend money to roll numbers, those numbers will be the amount of money you gain
- at end of each set of rolls, player will need variable amount of money to progress, otherwise fail
- player can buy power-ups with money to make numbers give more money
- game can continue on infinitely
gameplay:
- game has 5 number slots to roll, beginning from 0-9
- game checks every 10 rolls to see if player is past threshold, threshold gets exponentially larger
- shop will have power-ups to boost numbers, increase odds of certain numbers, etc
shop:
- power-ups:
    - xN: multiplies all number values by N for one slot
    - xN(1): multiplies one number by N for one slot (big multiplier)
    - +N: adds N to all number values for one slot
    - +N(1): adds N to one number for one slot (big addition)
    - +X%: makes the biggest number +X% more likely to show up
    - =N: sets one number to N for one slot
- modifiers (expensive)                                                                        --MULTIPLIERS NOT FINAL--
    - isPrime: if N values are prime numbers in a roll, multiply sum of rolls by N+1
    - inOrder/inReverse: if the values are increasing/decreasing from left->right, multiply sum of rolls by 10
    - pythagorean: if three numbers make up a pythagorean triple, multiply sum of rolls by 20
    - isEven/isOdd: if at least 2 numbers are even/odd, multiply sum of rolls by 2
    - isDuplicate: (only applies if there are 2+ same numbers)
                   if N values are the same, multiply sum of rolls by 4**N
    -
"""
import os
import random
import sys
import time

from numpy.random import choice
from modifiers import *


class Slot:
    def __init__(self):
        self.nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.probability = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    def roll(self):
        return choice(self.nums, p=self.probability)

    def multiply_slot(self, mult: float) -> None:
        for i in range(len(self.nums)):
            self.nums[i] *= mult

    def add_slot(self, add: float) -> None:
        for i in range(len(self.nums)):
            self.nums[i] += add

    def multiply_num(self, mult: float, index: int) -> None:
        self.nums[index] *= mult

    def add_num(self, add: float, index: int) -> None:
        self.nums[index] += add

    def set_num(self, set_n: [int, float], index: int) -> None:
        self.nums[index] = set_n

    def add_percent(self, prob: float, index: int) -> None:
        self.probability[index] += prob

        for i in range(len(self.probability)):
            if self.probability[i] != index:
                self.probability[i] -= prob / 9


pow_list = ["x2", "x3", "x5", "x9", "x10", "x20", "x25",   # xN
            "x(1)10", "x(1)25", "x(1)50", "x(1)100",       # xN(1)
            "+5", "+10", "+25", "+50",                     # +N
            "+(1)25", "+(1)50", "+(1)100", "+(1)250",      # +N(1)
            "+%2", "+%5", "+%10", "+%20", "+%25", "+%50",  # +X%
            "=25", "=50", "=100", "=250", "=1000"]         # =N

mod_list = ["isPrime", "inOrder", "inReverse", "pythagorean", "isEven", "isOdd", "isDuplicate"]

mod_dict = {"isPrime": False,
            "inOrder": False,
            "inReverse": False,
            "pythagorean": False,
            "isEven": False,
            "isOdd": False,
            "isDuplicate": False}

pow_price_dict = {"x2": 5, "x3": 10, "x5": 40, "x9": 100, "x10": 150, "x20": 350, "x25": 500,
                  "x(1)10": 10, "x(1)25": 30, "x(1)50": 75, "x(1)100": 200,
                  "+5": 30, "+10": 75, "+25": 300, "+50": 1000,
                  "+(1)25": 50, "+(1)50": 125, "+(1)100": 350, "+(1)250": 1200,
                  "+%2": 200, "+%5": 650, "+%10": 1500, "+%20": 3500, "+%25": 5000, "+%50": 12500,
                  "=25": 40, "=50": 100, "=100": 250, "=250": 700, "=1000": 3000}


mod_price_dict = {"isPrime": 750,
                  "inOrder": 1500,
                  "inReverse": 1500,
                  "pythagorean": 3000,
                  "isEven": 450,
                  "isOdd": 450,
                  "isDuplicate": 7500}

failed = False
level = 1
roll_count = 0
money = 50
reset_cost = 100
slots = []
shop_list = ["", "", "",
             "", "", "",
             "", "", ""]

shop_dict = {}

for slot in range(5):  # creates 5 Slot objects
    slots.append(Slot())


# equation for threshold levels
def threshold_eq():  # temporary, will balance later
    return round(((level ** 2) + 100) * (level ** 1))


# equation for shop prices

def price_eq():  # temporary, will balance later
    return 1 + (2 ** (roll_count / 30))


# check if a specific modifier is already in the shop
def check_dupe(item, count):
    cur_count = 0

    for check_item in shop_list:
        if check_item.split() == item.split() and cur_count != count:
            return True
        cur_count += 1
    return False


# check if player has enough money every 10 rolls
def check_threshold():
    global level, money
    os.system("cls")
    if roll_count % 10 == 0:
        if money >= threshold_eq():
            print("you pass this level")
            money -= threshold_eq()
            level += 1
        else:
            print("you fail")
            time.sleep(3)
            sys.exit()


# string list with all possible power-ups
# another string list with all modifiers still available (haven't been bought yet)
# player will have a dict with all modifiers bought
_pos = -1


def shop(reset=False):
    global shop_list, reset_cost, money

    if reset:
        shop_dict.clear()
        shop_list = ["", "", "",
                     "", "", "",
                     "", "", ""]

        if money > reset_cost:
            money -= reset_cost
            reset_cost = reset_cost ** 2
        else:
            print("Not enough money to reset")

    i = 0
    cur_item = ""
    cur_item_price = 0

    if _pos > -1:
        shop_dict.pop(shop_list[_pos])
        shop_list.pop(_pos)

        shop_list.append("")

    # reset items in shop if player first enters shop or wants to
    for item in shop_list:
        if item == "" or reset:
            p = random.random()
            is_dupe = True

            while is_dupe:
                if p < 0.9:  # 90% for a power-up
                    cur_item = shop_list[i] = random.choice(pow_list)
                    cur_item_price = pow_price_dict.get(cur_item)
                elif p >= 0.9:  # 10% for a modifier
                    bought_mod = True
                    while bought_mod:  # check if the mod is already bought and re-rolls
                        check_item = shop_list[i] = random.choice(mod_list)
                        if not mod_dict[check_item]:
                            cur_item = check_item
                            bought_mod = False
                    cur_item_price = mod_price_dict.get(cur_item)
                is_dupe = check_dupe(cur_item, i)

                shop_dict[shop_list[i]] = cur_item_price
        i += 1

    # update prices every time shop() is called
    for j in range(len(shop_dict)):
        in_pow = False

        for k in range(len(pow_list)):
            if shop_list[j] == pow_list[k]:
                in_pow = True
                shop_dict[shop_list[j]] = round(pow_price_dict.get(shop_list[j]) * price_eq())
        if not in_pow:
            for m in range(len(mod_list)):
                if shop_list[j] == mod_list[m]:
                    shop_dict[shop_list[j]] = round(mod_price_dict.get(shop_list[j]) * price_eq())

    i = 1
    for item in shop_dict:
        print(f"{i}: {item} - {shop_dict[item]}")
        i += 1

    valid_nums = False

    # check if numbers are within range of shop slots
    while not valid_nums:
        resp = input("Pick the item you want (1-9 or 'EXIT'): ")
        if resp.upper() == "EXIT":
            break
        elif 0 < int(resp) <= 9:
            valid_nums = True
            buy_item(int(resp))
        else:
            print("Invalid number")


# returns price
def buy_item(pos):
    global money, _pos
    adjusted_pos = pos - 1
    item = shop_list[adjusted_pos]
    price = shop_dict[shop_list[adjusted_pos]]

    if money >= price:
        # cases for each upgrade
        match item:
            # region cases for power-ups
            case ("x2" | "x3" | "x5" | "x9" | "x10" | "x20" | "x25"):
                apply_slot("*", int(item[1:]))
            case ("x(1)10" | "x(1)25" | "x(1)50" | "x(1)100"):
                apply_num("*", int(item[4:]))
            case ("+5" | "+10" | "+25" | "+50"):
                apply_slot("+", int(item[1:]))
            case ("+(1)25" | "+(1)50" | "+(1)100" | "+(1)250"):
                apply_num("+", int(item[4:]))
            case ("+%2" | "+%5" | "+%10" | "+%20" | "+%25" | "+%50"):
                apply_num("%", int(item[2:]) / 100)
            case ("=25" | "=50" | "=100" | "=250" | "=1000"):
                apply_num("=", int(item[1:]))
            # endregion
            # region cases for modifiers
            case "isPrime":
                mod_dict["isPrime"] = True
            case "inOrder":
                mod_dict["inOrder"] = True
            case "inReverse":
                mod_dict["inReverse"] = True
            case "pythagorean":
                mod_dict["pythagorean"] = True
            case "isEven":
                mod_dict["isEven"] = True
            case "isOdd":
                mod_dict["isOdd"] = True
            case "isDuplicate":
                mod_dict["isDuplicate"] = True
            # endregion
        money -= price
        _pos = adjusted_pos
    else:
        print("not enough money")


def apply_slot(operator: str, num: float) -> None:
    in_range = False
    i = 0
    while not in_range:
        i = int(input("Which slot do you want to apply this power-up to?: "))
        if 1 <= i <= 5:
            in_range = True
        else:
            print("invalid number")

    _slot = slots[i - 1]

    if operator == "*":
        _slot.multiply_slot(num)
    elif operator == "+":
        _slot.add_slot(num)


def apply_num(operator: str, num: float) -> None:
    in_range_slot = False
    in_range_num = False
    slot_n = 0
    i = 0
    while not in_range_slot:
        slot_n = int(input("Which slot do you want to apply this power-up to?: "))
        if 1 <= slot_n <= 5:
            in_range_slot = True
            while not in_range_num:
                i = int(input("Which number do you want to apply this power-up to?: "))
                if 1 <= i <= 10:
                    in_range_num = True
                else:
                    print("invalid number")
        else:
            print("invalid number")

    _slot = slots[slot_n - 1]

    if operator == "*":
        _slot.multiply_num(num, i - 1)
    elif operator == "+":
        _slot.add_num(num, i - 1)
    elif operator == "=":
        _slot.set_num(num, i - 1)
    elif operator == "%":
        _slot.add_percent(num, i - 1)


# calculates all modifiers and applies multiplier (modifiers are multiplicative)
def apply_mods(roll_lst):
    mult = 1
    if mod_dict["isPrime"]:
        mult *= is_prime(roll_lst)
    if mod_dict["inOrder"]:
        mult *= in_order(roll_lst)
    if mod_dict["inReverse"]:
        mult *= in_reverse(roll_lst)
    if mod_dict["pythagorean"]:
        mult *= pythagorean(roll_lst)
    if mod_dict["isEven"]:
        mult *= is_even(roll_lst)
    if mod_dict["isOdd"]:
        mult *= is_odd(roll_lst)
    if mod_dict["isDuplicate"]:
        mult *= is_duplicate(roll_lst)

    return mult


# main
print("Game Start")
while not failed:
    print("Rolls: " + str(roll_count))
    print("Money needed: " + str(threshold_eq()))
    print("Money: " + str(money))

    main_resp = input(f"Press ENTER to roll or type 'BUY' or 'RESET ({reset_cost})' to enter shop: ")
    os.system("cls")
    if main_resp.upper() == "":
        roll_count += 1
        rolls = []
        money_gained = 0

        for slot in slots:
            result = slot.roll()
            rolls.append(result)
            money_gained += result

        money_gained *= apply_mods(rolls)

        money += money_gained

        print(rolls)

        check_threshold()

    elif main_resp.upper() == "BUY":
        shop()
    elif main_resp.upper() == "RESET":
        shop(reset=True)
