# def greet(name):
#     print(f"Hello, {name}!")

# user_name = input("Enter your name: ")

# greet(user_name)

# if unsorted_numbers[i] > unsorted_numbers[i + 1]:

Current = int(input("enter current value"))
Resistance = 5 

Heat = (Current * Current) * Resistance

def greet(name):
     print(f"Hello, {name}!")

print("Electric Heat:", Heat, "J")

if Heat > 500:
    greet("Red")
   
else: 
    print("Green Danger")    