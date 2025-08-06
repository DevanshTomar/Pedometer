# 🚶‍♂️ Pedometer - Real-World Step Counter

A Python implementation of a pedometer that processes accelerometer data to count steps, similar to how fitness trackers and smartphones work. This project demonstrates real-world signal processing techniques to extract meaningful information from noisy sensor data.

## 🎯 What It Does

This application takes raw accelerometer data (x,y,z motion readings from phone sensors) and uses signal processing algorithms to detect walking patterns and count steps. It essentially replicates what your phone's built-in step counter does - identifying the characteristic up-and-down bounce of human walking to count each footstep.

## 🌟 Features

- **Dual Format Support**: Accepts both combined (total acceleration) and separated (user + gravity) data formats
- **Signal Processing Pipeline**: Filters noise and isolates step patterns using IIR filters
- **Smart Step Detection**: Uses threshold crossing with hysteresis to avoid counting false steps
- **Web Interface**: User-friendly upload and analysis interface
- **Metrics Calculation**: Computes distance traveled, walking time, and accuracy
- **Visualization**: Generates plots showing the signal processing stages
- **Modular Design**: Clean, maintainable code structure for easy customization

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/pedometer.git
cd pedometer
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

## 📊 Data Format

### Combined Format (Most Common)
Total acceleration in x,y,z directions:
```
x1,y1,z1;x2,y2,z2;x3,y3,z3;...
```
Example:
```
0.1,-0.98,0.02;0.12,-0.95,0.03;0.11,-0.99,0.01;...
```

### Separated Format (Advanced)
User acceleration and gravitational acceleration separated:
```
xu1,yu1,zu1|xg1,yg1,zg1;xu2,yu2,zu2|xg2,yg2,zg2;...
```

## 📁 Project Structure

```
pedometer_project/
├── app.py                 # Flask web application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── core/                  # Signal processing algorithms
│   ├── filters.py         # IIR filter implementations
│   ├── parser.py          # Data format parser
│   ├── processor.py       # Signal processor
│   ├── analyzer.py        # Step counter
│   └── pipeline.py        # Processing pipeline
├── models/                # Data models
│   ├── user.py           # User information
│   └── trial.py          # Trial metadata
├── utils/                 # Utilities
│   ├── file_handler.py   # File management
│   └── data_generator.py # Sample data generation
├── templates/            # HTML templates
├── static/              # CSS styles
├── uploads/             # Uploaded data files
└── example_data/        # Sample data
```

## 🔧 How It Works

### Signal Processing Pipeline

1. **Parse Data**: Convert raw accelerometer data to standard format
2. **Separate Gravity**: Use low-pass filter to extract gravitational component
3. **Isolate Movement**: Calculate dot product to get movement in gravity direction
4. **Filter Noise**: Apply filters to remove high-frequency noise and drift
5. **Count Steps**: Detect peaks using threshold crossing with hysteresis

### Algorithm Details

```python
# 1. Separate gravity from user movement
gravitational_accel = low_pass_filter(total_accel, 0.2_Hz)
user_accel = total_accel - gravitational_accel

# 2. Get movement in gravity direction
bounce_signal = dot_product(user_accel, gravitational_accel)

# 3. Clean the signal
filtered = low_pass_filter(bounce_signal, 5_Hz)  # Remove noise
filtered = high_pass_filter(filtered, 1_Hz)      # Remove drift

# 4. Count threshold crossings
steps = count_peaks(filtered, threshold=0.09)
```

## 🧪 Testing

### Use Sample Data
The application automatically generates a 10-second walking sample:
```
example_data/walking_data.txt
```

### Create Test Data
```python
python -c "from utils.data_generator import generate_example_data; print(generate_example_data())" > test.txt
```

### Expected Results
- Sample Rate: 100 Hz
- Duration: 10 seconds
- Expected Steps: ~20 steps (2 steps/second)

## 📈 Customization

### Adjust Step Sensitivity
Edit `config.py`:
```python
STEP_THRESHOLD = 0.09  # Increase for less sensitive detection
```

### Change Filter Parameters
Modify filter coefficients in `config.py` for different walking patterns or sampling rates.

### Add New Features
The modular structure makes it easy to add:
- New filter types in `core/filters.py`
- Additional metrics in `core/analyzer.py`
- Different visualizations in `utils/data_generator.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Technical Background

This implementation is based on the article ["A Pedometer in the Real World"](https://aosabook.org/en/500L/a-pedometer-in-the-real-world.html) from "500 Lines or Less". It demonstrates:

- **Digital Signal Processing**: IIR filters for frequency-based signal separation
- **Linear Algebra**: Dot product for directional movement extraction
- **Algorithm Design**: Hysteresis for robust peak detection
- **Software Engineering**: Modular design with separation of concerns

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid literal for int()"**: Leave optional fields empty instead of entering invalid values
2. **"Bad Input" error**: Check data format - must be comma and semicolon separated
3. **No steps detected**: Ensure data contains walking motion, not stationary readings
4. **Too many steps**: Adjust `STEP_THRESHOLD` in `config.py`

### Debug Mode
Run with debug output:
```python
app.run(debug=True)  # Already enabled by default
```


## 🙏 Acknowledgments

- Original article: "A Pedometer in the Real World" by Dessy Daskalov
- The Architecture of Open Source Applications (AOSABOOK)
- Signal processing concepts from digital signal processing literature
