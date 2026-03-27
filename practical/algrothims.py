un = [14, 7, 3, 1, 2, 9, 8, 0, 6, 4, 5]
print("Before Swap:", un)

x1 = len(un)



for x in range (9):
  for y in range(10):
    print(un[y])

    if un[y] > un[y + 1]:
     print("smaller:", un[y + 1])
     print("bigger:", un[y])

     x1 = un[y + 1]
     y1 = un[y]

     un[y + 1] = y1
     un[y] = x1
     






 
x1 = 0
y1 = 7

x = un[x1] 
y = un[y1] 
if x > y:   
 un[x1] = y
 un[y1] = x
else:
 un[y1] = y
 un[x1] = x

print("After Swap:", un)



# fill up the array index such that when you change the variables
# all the index automatically change according to the value of the variable

