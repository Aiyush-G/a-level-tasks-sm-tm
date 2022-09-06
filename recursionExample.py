# Sum to number: 2 returns 3 (1+2)
def sum_to_n(n):
    if n==1:
        return 1
    else:
        return n+sum_to_n(n-1)

n = int(input("n="))
print(sum_to_n(n))