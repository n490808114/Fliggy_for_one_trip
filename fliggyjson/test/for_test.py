g = [1,2,3,4]
print(id(g))
def add(a,b):
    return a + b
for n in[2,10]:
    print(n,list(g),id(g),'0001')
    g = (add(n,i) for i in g)
    print(n,list(g),id(g),'0002')
print(list(g))