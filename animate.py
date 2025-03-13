import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.transforms import Affine2D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

class Mug:
    def __init__(self, ax, radius=0.2, handleSize=(0.16, 0.06)):
        self.ax = ax
        self.radius = radius
        self.handleSize = handleSize
        
        self.body = Circle((0, 0), self.radius, color='gray', fill=True)
        self.ax.add_patch(self.body)
        self.handle = Rectangle((0, 0), self.handleSize[0], self.handleSize[1], color='gray', fill=True)
        self.ax.add_patch(self.handle)

    def update(self, angle, position):
        self.body.center = position
        self.handle.set_x(position[0] + self.radius)
        self.handle.set_y(position[1] - self.handleSize[1]/2)

        transform = Affine2D().rotate_around(*position, angle)
        self.handle.set_transform(transform + self.ax.transData)

        return self.body, self.handle
    

class MicrowaveMugAnimation:
    def __init__(self):
        # Initialize figure and axis
        bound = 1.5
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        self.ax.set_xlim(-bound, bound)
        self.ax.set_ylim(-bound, bound)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # Microwave plate (circle)
        self.plate = Circle((0, 0), 1.3, color='gray', fill=False, linewidth=2)
        self.ax.add_patch(self.plate)

        # The mug
        self.mug = Mug(self.ax)
        self.rotationRate = 1.0
        self.revRadius = 0.9

        # The slider to control mug rotations
        self.ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
        self.slider = Slider(self.ax_slider, 'Mug rotation speed', 0, 2, valinit = 1, valstep = 0.05)
        self.slider.on_changed(self.update_slider)
        
        # Start animation
        self.ani = FuncAnimation(self.fig, self.update, frames=10000, interval=20, blit=False)
        plt.show()
    
    def update(self, frame):
        self.revAngle = frame * np.pi / 60  # Convert frame to angle
        position = (self.revRadius*np.cos(self.revAngle), self.revRadius*np.sin(self.revAngle))
        rotAngle = self.rotationRate * frame * np.pi / 60

        return self.mug.update(rotAngle, position)
    
    def update_slider(self, val):
        self.rotationRate = self.slider.val


if __name__ == "__main__":
    MicrowaveMugAnimation()
