L1 = ['a', 'b', 'c']
L2 = ['b', 'd']

print ("Common Elements")
print (set(L1)-(set(L1)-set(L2)))

print ("Elements in L1 not in L2")
print (set(L1)-set(L2))
