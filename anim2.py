import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

class MicrowaveMugAnimation:
    def __init__(self):
        # Initialize figure and axis
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # Microwave plate (circle)
        self.plate = plt.Circle((0, 0), 1, color='gray', fill=False, linewidth=2)
        self.ax.add_patch(self.plate)

        # Mug properties
        self.mug_radius = 0.1  # Radius of the mug
        self.handle_offset = 0.12  # Offset for handle
        self.handle_size = (0.05, 0.02)  # Width and height of handle
        
        # Initial conditions
        self.rotation_factor = 1.0
        self.angle = 0  # Initial angle for revolution
        self.auto_mode_active = False  # Flag to track auto mode

        # Create mug body as a circle
        self.mug_body = Circle((0, 0), self.mug_radius, color='blue', label='Mug')
        self.ax.add_patch(self.mug_body)
        
        # Create mug handle as a small rectangle
        self.handle = Rectangle((0, 0), self.handle_size[0], self.handle_size[1], color='black', label='Handle')
        self.ax.add_patch(self.handle)
        
        # Create slider
        self.ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
        self.slider = Slider(self.ax_slider, 'Rotation Factor', 0, 2, valinit=1, valstep=0.05)
        self.slider.on_changed(self.update_slider)
        
        # Auto mode button
        self.ax_button = plt.axes([0.8, 0.02, 0.1, 0.05])
        self.button = Button(self.ax_button, 'Auto')
        self.button.on_clicked(self.auto_mode)
        
        # Start animation
        self.ani = FuncAnimation(self.fig, self.update, frames=120, interval=50, blit=False)
        plt.legend()
        plt.show()
    
    def update(self, frame):
        self.angle = frame * np.pi / 30  # Convert frame to angle
        
        # Mug position (revolves around plate)
        mug_x, mug_y = np.cos(self.angle), np.sin(self.angle)
        self.mug_body.center = (mug_x, mug_y)
        
        # If auto mode is active, gradually increase rotation factor
        if self.auto_mode_active:
            self.rotation_factor = min(2, self.rotation_factor + 0.02)  # Increments smoothly
            self.slider.set_val(self.rotation_factor)
        
        # Rotation of mug
        mug_rotation = self.rotation_factor * self.angle  # Rotation relative to revolution
        handle_x = mug_x + self.handle_offset * np.cos(mug_rotation) - self.handle_size[0] / 2
        handle_y = mug_y + self.handle_offset * np.sin(mug_rotation) - self.handle_size[1] / 2
        self.handle.set_xy((handle_x, handle_y))
        
        return self.mug_body, self.handle
    
    def update_slider(self, val):
        self.rotation_factor = self.slider.val
        self.auto_mode_active = False  # Disable auto mode if user manually adjusts the slider
    
    def auto_mode(self, event):
        if not self.auto_mode_active:
            self.auto_mode_active = True  # Activate auto mode

if __name__ == "__main__":
    MicrowaveMugAnimation()
