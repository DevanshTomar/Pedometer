import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def generate_example_data():
    """Generate example accelerometer data for testing"""
    sampling_rate = 100  # Hz
    duration = 10  # seconds
    samples = sampling_rate * duration
    
    data_points = []
    for i in range(samples):
        t = i / sampling_rate
        step_frequency = 2  # Hz (2 steps per second)
        
        x = 0.1 * math.sin(2 * math.pi * step_frequency * t) + np.random.normal(0, 0.02)
        y = -1.0 + 0.3 * math.sin(2 * math.pi * step_frequency * t) + np.random.normal(0, 0.03)
        z = 0.05 * math.sin(4 * math.pi * step_frequency * t) + np.random.normal(0, 0.02)
        
        data_points.append(f"{x:.6f},{y:.6f},{z:.6f}")
    
    return ';'.join(data_points)

def create_plot(data, title):
    """Create a plot and return it as base64 encoded string"""
    plt.figure(figsize=(10, 4))
    plt.plot(data)
    plt.title(title)
    plt.xlabel('Sample')
    plt.ylabel('Acceleration (g)')
    plt.grid(True)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url