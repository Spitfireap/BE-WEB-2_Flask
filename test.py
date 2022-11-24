a = 1024
b = bin(a)
liste = []
for charactere in str(b)[2:]:
    liste.append(int(charactere))

print(liste) # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]