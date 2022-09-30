_list = [
    [6, 7, 8],
    [3, 7, 1,],
    [0, 7, 2],
]

# print(_list[1][0])

for i in _list:
    vals, currColumn = [], _list.index(i)
    for j in range(0,len(i)):
        curr = _list[j][_list.index(i)]
        print(curr)
        vals.append(curr)
    if all(x==vals[0] for x in vals) and vals[0] != None: 
        print(f"Column {currColumn} has 3 in a row")
    vals.clear()
