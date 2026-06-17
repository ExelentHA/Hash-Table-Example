from time import perf_counter
from tqdm import tqdm

file = 'akjv.txt'

buf = None
with open(file) as f:
    buf = f.read()
print(f"size of the file: {len(buf)/1024**2:.2f}mb")

collection = []

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

# O(n^2) or O(m×n)
start = perf_counter()
for i in tqdm(range(0, len(buf))):
    if not check_if_exist(buf[i]):
        collection.append([buf[i], 1])
    else:
        increment(buf[i])
total = perf_counter() - start

collection.sort()

n = 0
for i in collection:
    n += 1
    print(f'indx: {n}, char: {i[0].encode()}, count: {i[1]}')

print(f'Time elapse: {total:.2f}sec')
