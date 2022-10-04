# Sum to number: 2 returns 3 (1+2)
def sum_to_n(n):
    if n==1:
        return 1
    else:
        return n+sum_to_n(n-1)

def sum_to_n_itterative(n):
    x = 0
    for turn in range(0, n+1):
        x += turn       
    return x

print(sum_to_n_itterative(7))
