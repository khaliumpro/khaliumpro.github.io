# Heapify function: makes sure the subtree follows max-heap rules
def heapify(arr, heap_size, root_index):

    # Step 1: Assume root is the largest
    largest = root_index

    # Calculate left and right child indices
    left_child = 2 * root_index + 1
    right_child = 2 * root_index + 2

    # Step 2: Check if left child exists and is greater
    if left_child < heap_size and arr[left_child] > arr[largest]:
        largest = left_child

    # Step 3: Check if right child exists and is greater
    if right_child < heap_size and arr[right_child] > arr[largest]:
        largest = right_child

    # Step 4: If the largest is not the root, swap
    if largest != root_index:
        temp = arr[root_index]
        arr[root_index] = arr[largest]
        arr[largest] = temp

        # Step 5: Recursively fix the affected subtree
        heapify(arr, heap_size, largest)


# Main heap sort function
def heap_sort(arr):

    n = len(arr)

    # Step 1: Build the max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Step 2: Extract elements one by one
    for i in range(n - 1, 0, -1):

        # Move current largest (root) to the end
        temp = arr[0]
        arr[0] = arr[i]
        arr[i] = temp

        # Fix the heap again (reduced size)
        heapify(arr, i, 0)

    return arr


# ----------- TESTING -----------

my_array = [8, 4, 9, 12, 11]

print("Original:", my_array)

heap_sort(my_array)

print("Sorted:", my_array)