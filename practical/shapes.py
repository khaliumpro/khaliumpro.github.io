
def calculate_square_area(x, y):
    area = x * y
    return area

side_of_square = 10
side_of_squaree = 10
result = calculate_square_area(side_of_squaree, side_of_squaree)
print("Area of Square 1:", result, "m**2")

result = calculate_square_area(20, 20 ,)
print("Area of Square 2:", result, "m**2")

def compute_triangle_area(b, h):
    area = 0.5 * (b * h)
    return area

b = 10
h = 4

print("Area of Triangle 1:", compute_triangle_area(b, h), "m**2" )
print("Area of Triangle 2:", compute_triangle_area(10, 10), "m**2" )


def determine_missing_angle_of_triangle(x1, x2):
    x3 = 180 - (x1 + x2)
    return x3
 
angle_x1 = input()
print("Missing Angle of Tringle:", determine_missing_angle_of_triangle(10, 20), "degrees")


""
def evaluate_specific_heat_capacity(m, t2, t1):
    specific_heat_capacity = h / m * (t2 - t1)
    return specific_heat_capacity
booc = evaluate_specific_heat_capacity(66, 5, 4)
print("Specific Heat Capacity", evaluate_specific_heat_capacity(10, 3, booc) )







