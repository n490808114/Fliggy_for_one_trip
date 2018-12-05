g = [1,2,3,4]
def add(a,b):
    return a + b
for n in[2,10]:
	g = (add(n,i) for i in g)
print(list(g))