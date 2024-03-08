import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def print_selected_points():
    for point in selectedPoints:
        print(f"({point.x}, {point.y})")
    print()

class InteractivePlot(object):
    zoomFactor = 0.5
    def __init__(self, x, y):
        self.fig, self.ax = plt.subplots()
        self.ax.plot(x, y, label='Data')
        self.ax.set_xlabel(' ')
        self.ax.set_ylabel(' ')
        self.ax.grid(True)
        self.ax.legend()

        # Add cursor functionality
        self.cursor = CursorClass(self.ax, x, y, self)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.cursor.motion_event)
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.cursor.click_event)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key_event)

        # Initialize list to store points indicated by hovering
        self.indicated_points = []

    def show_plot(self):
        plt.show()

    def on_key_event(self, event):
        if event.key == 'p':
            with open('selected_points.csv', 'w') as file:
                file.write(f"")
            selectedPoints.clear()
        if event.key == 'z':
            # Zoom at the cursor position
            if self.zoomFactor > 0.1:
                self.zoomFactor -= 0.1
            self.zoom_at_cursor()
        if event.key == 'x':
            # Zoom at the cursor position
            if self.zoomFactor < 0.9:
                self.zoomFactor += 0.1
            self.zoom_at_cursor()

    def zoom_at_cursor(self):
        print(f"Zoom factor: {self.zoomFactor}")
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        x = self.cursor.get_cursor_position()
        
        # Set new limits for x around the cursor position
        new_xlim = (x - x*self.zoomFactor, x + x*self.zoomFactor)

        # Set new limits and redraw the plot
        self.ax.set_xlim(new_xlim)
        self.ax.figure.canvas.draw_idle()
        
    def plot_point(self, point):
        selectedPoints.append(point)
        plt.scatter(point.x, point.y, color='red', marker='x', s=100)
        plt.text(point.x + 0.1, point.y + 0.1, f"({point.x}, {point.y})")
    def unplot_point(self):
        if selectedPoints:
            print_selected_points()
            point = selectedPoints.pop()
            # Remove the plotted point from the plot
            scatter_plot = self.ax.scatter([point.x], [point.y], color='red', marker='x', s=100)
            scatter_plot.remove()
            self.ax.figure.canvas.draw_idle()

class CursorClass(object):
    def __init__(self, ax, x, y, interactive_plot):
        self.ax = ax
        self.ly = ax.axvline(color='red', alpha=0.5)
        self.marker, = ax.plot([0], [0], marker="x", color="red", zorder=3)
        self.x = x
        self.y = y
        self.txt = ax.text(0.7, 0.9, '')
        self.interactive_plot = interactive_plot

    def motion_event(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            indx = np.searchsorted(self.x, [x])[0]
            x = self.x[indx]
            y = self.y[indx]
            self.ly.set_xdata(x)
            self.marker.set_data([x], [y])
            self.txt.set_text('x=%1.3f, y=%1.3f' % (x, y))
            self.txt.set_position((x, y))
            self.ax.figure.canvas.draw_idle()
        
    def click_event(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            indx = np.searchsorted(self.x, [x])[0]
            x = self.x[indx]
            y = self.y[indx]

            if event.button == 1:  # Left click
                # Save indicated point when clicking
                self.interactive_plot.indicated_points.append((x, y))
                with open('selected_points.csv', 'a') as file:
                    file.write(f"{x}, {y}\n")
                self.interactive_plot.plot_point(Point(x, y))
            elif event.button == 3:  # Right click
                # Remove indicated point when right-clicking
                self.interactive_plot.unplot_point()
                
    def get_cursor_position(self):
        # Return current cursor position
        return self.marker.get_data()[0][0]

# Load your data from 'date.csv'
csvFile = pd.read_csv('date.csv')
# print(csvFile)

time = csvFile.iloc[:, 0]
value = csvFile.iloc[:, 1]

xpoints = np.array(time)
ypoints = np.array(value)

selectedPoints = []

# Create an instance of InteractivePlot
interactive_plot = InteractivePlot(xpoints, ypoints)

# Show the plot
interactive_plot.show_plot()

