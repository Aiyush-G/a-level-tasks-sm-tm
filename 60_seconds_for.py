# 60 Seconds for loop

_list = [1,24,23,21,4,5,123,23,2]
toFind = 21

for index in range(0,len(_list)):
    if _list[index] == toFind:
        print(f"Found {toFind} at position {index} in array.")
