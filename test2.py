import matplotlib.pyplot as plt

# Sample data
x_values = [2, 4, 6, 8]
y_values = [3, 5, 7, 9]

# Plotting points
plt.plot(x_values, y_values, 'o', label='Points')

# Function to unplot a point by its coordinates
def unplot_point(x, y):
    index_to_remove = None
    for i, (x_val, y_val) in enumerate(zip(x_values, y_values)):
        if x_val == x and y_val == y:
            index_to_remove = i
            break

    if index_to_remove is not None:
        x_values.pop(index_to_remove)
        y_values.pop(index_to_remove)
        plt.clf()
        plt.plot(x_values, y_values, 'o', label='Points')
        plt.legend()

# Unplotting a point
plt.show()
unplot_point(6, 7)
unplot_point(2, 3)
plt.show()