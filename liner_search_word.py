from time import perf_counter
from operator import itemgetter
from re import findall

file = 'akjv.txt'

buf = None
with open(file) as f:
    buf = f.read()
print(f"size of the file: {len(buf)/1024**2:.2f}mb")

# parse by words
buf = findall(r"[A-Za-z]+(?:'[A-Za-z]+)*", buf.strip())

collection = []

print(f"Total Tokens: {len(buf)}")

# O(n)
def check_if_exist(char : str):
    for i in range(0, len(collection)):
        if char == collection[i][0]:
            return True
    return False

# O(n)
def increment(char : str):
    for i in range(0, len(collection)):
        if char == collection[i][0]:
            collection[i][1] += 1

cclk = 0
tkc = 0
def updateStatus():
    global cclk
    clk = perf_counter()
    if clk > cclk:
        print(f"Evaluated Tokens: {len(collection)}, Token Left: {len(buf) - tkc}")
        cclk = clk + 10 # update every 10s 


# O(n^2) or O(m×n)
start = perf_counter()
for i in buf:
    tkc += 1
    updateStatus()
    if not check_if_exist(i):
        collection.append([i, 1])
    else:
        increment(i)
total = perf_counter() - start

collection.sort(key=itemgetter(1), reverse=True)

n = 0
for i in collection:
    n += 1
    print(f'indx: {n}, char: {i[0].encode()}, count: {i[1]}')
print(f'Time elapse: {total:.2f}sec')


# 738.71sec 
