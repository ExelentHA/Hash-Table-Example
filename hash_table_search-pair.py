from time import perf_counter
from operator import itemgetter

file = 'akjv.txt'

buf = None
with open(file) as f:
    buf = f.read()
print(f"size of the file: {len(buf)/1024**2:.2f}mb")

collection = []

N = 10000

arr = [['', 0, False] for i in range(N)]

def hashed(char : str):
    return None

def djb2(tok : str): # djb2 hashing algo
    hash = 5381;
    for c in range(len(tok)):
        hash = hash * 33 + ord(tok[c])
    return hash;


def open_add(key : int, chars : str):
    c = 0 # if we iterate thru the arr and 
          # we cant find an available slot
          # we throw an error
    while True: # Open Addressing | Liner Probing
        key = (key + 1)%N # key%N is overflow guard
        c+=1
        if c > N:
            print("No space left")
            exit(1)
        if arr[key][0] == chars:
            arr[key][1] += 1
            break
        elif not arr[key][2]:
            arr[key] = [chars, 1, True]
            break

# O(n^2) or O(m×n)
stp = 2
col_c = 0
start = perf_counter()
for i in range(0, len(buf), stp):
    if i+stp > len(buf):
        break
    pair = buf[i]+buf[i+1]
    key = djb2(pair)%N
    if arr[key][2]: # occupied scenario
        if not arr[key][0] == pair: # collided
            col_c += 1
            open_add(key, pair)
        else:
            arr[key][1] += 1
    else: # unoccupied scenario
        arr[key] = [pair, 1, True]
total = perf_counter() - start

occ = [v for v in arr if v[2]]
occ.sort(key=itemgetter(1), reverse=True)
print("Top 10 frequent pair")
for i,v in enumerate(occ):
    if i > 10:
        break
    print(f'indx: {i}, pair: "{v[0].encode()}", count: {v[1]}')
print(f'Hash collisons: {col_c}')
print(f'Unique tokens: {len(occ)}')
print(f'Time elapse: {total:.2f}sec')
