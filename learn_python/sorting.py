
Current = int(input("enter current value"))
unsorted_numbers = [5, 2, Current, 1, 5, 6]


print(unsorted_numbers[2])
print("How many numbers in the llst", len(unsorted_numbers))
lngth = len (unsorted_numbers)
print(lngth)
Current = int(input("enter current value"))
for d in range(lngth):
    
    print("d", d)
    print(unsorted_numbers[d]+Current)