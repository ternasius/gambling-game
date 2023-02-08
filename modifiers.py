import math


def is_prime(roll_lst):
    count = 0
    for roll in roll_lst:
        prime = True
        for i in range(2, round(math.sqrt(roll))):
            if roll % i == 0:
                prime = False
        if prime:
            count += 1

    if count > 1:
        print(f"There are {count} primes in this set")
    elif count == 1:
        print(f"There is 1 prime in this set")

    count += 1  # this is the "+1" in "N+1"

    return count


def in_order(roll_lst):
    minimum = 0
    for roll in roll_lst:
        if roll < minimum:
            return 1
        minimum = roll

    print("This set is in order")

    return 10


def in_reverse(roll_lst):
    maximum = float("inf")
    for roll in roll_lst:
        if roll > maximum:
            return 1
        maximum = roll

    print("This set is in reverse order")

    return 10


def pythagorean(roll_lst):
    for i in range(len(roll_lst) - 1):
        for j in range(1, len(roll_lst)):
            num1 = roll_lst[i]
            num2 = roll_lst[j]
            for k in range(len(roll_lst)):
                if abs((num1 ** 2) + (num2 ** 2)) == roll_lst[k] ** 2:

                    print(f"There is a pythagorean triple in this set: {num1}, {num2}, {roll_lst[k]}")

                    return 20
    return 1


def is_even(roll_lst):
    count = 0
    for roll in roll_lst:
        if roll % 2 == 0:
            count += 1
    if count >= 2:

        print(f"There are {count} even numbers in this set")

        return 2

    return 1


def is_odd(roll_lst):
    count = 0
    for roll in roll_lst:
        if roll % 2 != 0:
            count += 1
    if count >= 2:

        print(f"There are {count} odd numbers in this set")

        return 2

    return 1


def is_duplicate(roll_lst):
    maximum = 0
    for roll1 in roll_lst:
        count = 0
        for roll2 in roll_lst:
            if roll1 == roll2:
                count += 1
        if count > maximum:
            maximum = count
    if maximum >= 2:

        print(f"There are {maximum} duplicate numbers in this set")

        return 4 ** maximum

    return 1
