# 60 Seconds Nested

# If we list all the natural numbers below 10 that are multiples of 3 or 5
#, we get 3, 5, 6 and 9. The sum of these multiples is 23.

# Find the sum of all the multiples of 3 or 5 for every item in array.

maxes = [1000, 500, 400, 200]
_max = 1000
divisor1, divisor2 = 3, 5
nums = []
total = 0

for _max in maxes:
    for x in range(_max-1, 0, -1):
        if x%divisor1 == 0 or x%divisor2 == 0:
            nums.append(x)

    for item in nums: total = total + item
    print(f"Sum of 3 or 5's below {_max} is: {total}")
    total = 0



