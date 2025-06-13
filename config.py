# Configuration settings for the pedometer application

# Filter coefficients
COEFFICIENTS_LOW_0_HZ = {
    'alpha': [1, -1.979133761292768, 0.979521463540373],
    'beta': [0.000086384997973502, 0.000172769995947004, 0.000086384997973502]
}

COEFFICIENTS_LOW_5_HZ = {
    'alpha': [1, -1.80898117793047, 0.827224480562408],
    'beta': [0.095465967120306, -0.172688631608676, 0.095465967120306]
}

COEFFICIENTS_HIGH_1_HZ = {
    'alpha': [1, -1.905384612118461, 0.910092542787947],
    'beta': [0.953986986993339, -1.907503180919730, 0.953986986993339]
}

# Analyzer settings
STEP_THRESHOLD = 0.09

# User defaults
GENDER_OPTIONS = ['male', 'female']
STRIDE_MULTIPLIERS = {'female': 0.413, 'male': 0.415}
AVERAGE_STRIDES = {'female': 70.0, 'male': 78.0}

# Upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

# Flask settings
SECRET_KEY = 'your-secret-key-here'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB