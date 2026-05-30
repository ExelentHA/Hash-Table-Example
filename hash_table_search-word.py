from time import perf_counter
from operator import itemgetter

file = 'akjv.txt'

buf = None
with open(file) as f:
    buf = f.read()
print(f"size of the file: {len(buf)/1024**2:.2f}mb")

N = 1000000

arr = [['', 0, False] for i in range(N)]

# O(1)
def cHash(tok : str): # custom hash
    return sum([ord(v) for v in tok]) * 33 + len(tok)

# O(1)
def djb2(tok : str): # djb2 hashing algo
    hash = 5381;
    for c in range(len(tok)):
        hash = hash * 33 + ord(tok[c])
    return hash;

# O(n)
def open_add(key : int, tok : str):
    c = 0 # if we iterate thru the arr and 
          # we cant find an available slot
          # we throw an error
    while True: # Open Addressing | Liner Probing
        key = (key + 1)%N # key%N is overflow guard
        c+=1
        if c > N:
            print("No space left")
            exit(1)
        if arr[key][0] == tok:
            arr[key][1] += 1
            break
        elif not arr[key][2]:
            arr[key] = [tok, 1, True]
            break

toks = [v for v in buf.strip().split()]
print(f"Token count {len(toks)}")
col_c = 0

# O(n^2) or O(m×n)
start = perf_counter()
for i in toks:
    key = djb2(i)%N # O(1)
    if arr[key][2]: # occupied scenario
        if arr[key][0] != i: # collided
            col_c += 1
            open_add(key, i) # O(n)
        else:
            arr[key][1] += 1
    else: # unoccupied scenario
        arr[key] = [i, 1, True]
total = perf_counter() - start

occ = [v for v in arr if v[2]] # filter occupied cells
# arr.sort() is O(nlog(n)) which is slow
occ.sort(key=itemgetter(1), reverse=True)
print("Top 10 frequent token")
for i,v in enumerate(occ):
    if i > 10:
        break
    print(f'indx: {i}, token: "{v[0]}", count: {v[1]}')
print(f'Hash collisons: {col_c}')
print(f'Unique tokens: {len(occ)}')
print(f'Time elapse: {total:.2f}sec')
