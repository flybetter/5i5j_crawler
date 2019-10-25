def splist(l, s):
    return [l[i:i + s] for i in range(len(l)) if i % s == 0]

list = range(14)
print(list)
data = round(len(list) / 3)
print(splist(list, data))

for i,v in enumerate(splist(list, data)):

    print(i,v)