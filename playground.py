__author__ = 'patrickjameswhite'
def distance(lista, listb):
    return sum( (b - a) ** 2 for a,b in zip(lista, listb) ) ** .5


def distance(lista, point):

    return sum((point- a) ** 2 for a in lista) ** .5
lista = [1,2,3,4,5,3,2,3,2]
listb = [2,3,4,5,6]
listc = [9,10,11,12,13]

print(distance(lista,3))
#print(distance(lista,listc))