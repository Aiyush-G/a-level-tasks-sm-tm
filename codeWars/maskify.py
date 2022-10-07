def maskify(cc):
    if len(cc) < 4:
        return cc
    hash = ""
    for x in range(0, len(cc)-4): hash += "#"
    toKeep = cc[len(cc) - 4:]
    return hash + toKeep