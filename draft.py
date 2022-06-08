from collections import defaultdict

d = defaultdict(int)
for i in range(10):
    d[i] += 1

for k in d.keys():
    print(k)
    