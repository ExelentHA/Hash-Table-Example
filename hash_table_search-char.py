from time import perf_counter
from operator import itemgetter
from tqdm import tqdm

file = 'akjv.txt'

buf = None
with open(file) as f:
    buf = f.read()
print(f"size of the file: {len(buf)/1024**2:.2f}mb")

N = 255

arr = [['', 0, False] for i in range(N)]

def hashed(char : str):
    return ord(char)

def open_add(key : int, char : str):
    c = 0 # if we iterate thru the arr and 
          # we cant find an available slot
          # we throw an error
    while True: # Open Addressing | Liner Probing
        key = (key + 1)%N # key%N is overflow guard
        c+=1
        if c > N:
            print("No space left")
            exit(1)
        if arr[key][0] == char:
            arr[key][1] += 1
            break
        elif not arr[key][2]:
            arr[key] = [char, 1, True]
            break

# O(m×n)
start = perf_counter()
for i in tqdm(buf):
    key = hashed(i)%N
    if arr[key][2]: # occupied scenario
        if not arr[key][0] == i: # collided
            open_add(key, i)
        else:
            arr[key][1] += 1
    else: # unoccupied scenario
        # init
        arr[key] = [i, 1, True]
total = perf_counter() - start

occ = [v for v in arr if v[2]]
occ.sort(key=itemgetter(1), reverse=True)
print('Top 10 frequent char:')
for i,v in enumerate(occ):
    if i > 10:
        break
    print(f'indx: {i} char: {v[0].encode()}, count: {v[1]}')
print(f'Time elapse: {total:.2f}sec')
