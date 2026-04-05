my_array = [100, 33, 44, 55, 66, 77, 88]

for i in range(len(my_array) - 1):
    min_index = i # i = 0 (100)

    # min_index smallest number on the right
    for j in range(i + 1, len(my_array)):
        print('j', j)
        # j = 1  (33)
        #minindx = 0 (100)
        if my_array[j] < my_array[min_index]:
            min_index = j

   
    temp = my_array[i] # my_array[i] larger number left
    my_array[i] = my_array[min_index] #smallest number right
    my_array[min_index] = temp