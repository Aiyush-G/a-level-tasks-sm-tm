# 60 Seconds while loop

import time as t # I had extra time :)

toCountTo = 19
current = 0 

while current != toCountTo:
    current += 1
    t.sleep(0.05)
    print(current)