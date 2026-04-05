my_array = [8, 4, 9, 12, 11]
  

    # Loop through the entire array
for i in range(len(my_array) - 1):

        # Step 1: Assume the current position is the minimum
        min_index = i

        # Step 2: Find the actual smallest element in the remaining array
        for j in range(i + 1, len(my_array)):
            if my_array[j] < my_array[min_index]:
                min_index = j

        # Step 3: Swap the found minimum with the current element
        if min_index != i:
            temp = my_array[i]          # store current value
            my_array[i] = my_array[min_index]  # replace with smallest found
            my_array[min_index] = temp   # put stored value in new position

print(my_array)