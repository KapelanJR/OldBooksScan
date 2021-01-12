import functools

k = [('f', 3), ('8', 4)]
ids = map(lambda x: x[1],k)
letters = map(lambda x: x[0], k)

letters = functools.reduce(lambda x,y: x+y,letters)
print(letters)
