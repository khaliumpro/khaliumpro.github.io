my_array = [8, 4, 9, 12, 11]

# this defined the given elements in the array
# After swapping all the numbers the second loop, the first loop allows you to iterate or loop over it again
for i in range(len(my_array)): 

    for j in range(len(my_array) -1):
        if my_array[j] > my_array[j + 1]:
            memory_left = my_array[j]
            memory_right = my_array[j + 1]

            my_array[j] = memory_right
            my_array[j + 1] = memory_left
print(my_array)

