import tkinter as tk

# Step 1: Create window
window = tk.Tk() 

# Step 2: Set title
window.title("My First App")

# Step 3: Add text (label)
label = tk.Label(window, text="Hello, Khalid!")
label.pack()

# Step 4: Run the app
window.mainloop()