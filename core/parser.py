from .filters import Filter

class Parser:
    """Parse accelerometer data from different formats"""
    
    def __init__(self, data):
        self.data = data
        self.parsed_data = None
    
    @classmethod
    def run(cls, data):
        parser = cls(data)
        parser.parse()
        return parser
    
    def parse(self):
        """Parse data into standard format"""
        try:
            # Split by semicolon for time series
            samples = self.data.strip().split(';')
            samples = [s for s in samples if s.strip()]
            
            # Parse each sample
            parsed_samples = []
            for sample in samples:
                if '|' in sample:  # Separated format
                    parts = sample.split('|')
                    user_accel = [float(x) for x in parts[0].split(',')]
                    grav_accel = [float(x) for x in parts[1].split(',')]
                    parsed_samples.append([user_accel, grav_accel])
                else:  # Combined format
                    total_accel = [float(x) for x in sample.split(',')]
                    parsed_samples.append([total_accel])
            
            # Validate data format
            for sample in parsed_samples:
                for accel in sample:
                    if len(accel) != 3:
                        raise ValueError('Bad Input. Ensure data is properly formatted.')
            
            # If combined format, split into user and gravitational acceleration
            if len(parsed_samples[0]) == 1:
                # Extract x, y, z components
                x_total = [s[0][0] for s in parsed_samples]
                y_total = [s[0][1] for s in parsed_samples]
                z_total = [s[0][2] for s in parsed_samples]
                
                # Apply low-pass filter to get gravitational acceleration
                x_grav = Filter.low_0_hz(x_total)
                y_grav = Filter.low_0_hz(y_total)
                z_grav = Filter.low_0_hz(z_total)
                
                # Calculate user acceleration
                x_user = [x_total[i] - x_grav[i] for i in range(len(x_total))]
                y_user = [y_total[i] - y_grav[i] for i in range(len(y_total))]
                z_user = [z_total[i] - z_grav[i] for i in range(len(z_total))]
                
                # Reformat to standard format
                self.parsed_data = []
                for i in range(len(parsed_samples)):
                    user = [x_user[i], y_user[i], z_user[i]]
                    grav = [x_grav[i], y_grav[i], z_grav[i]]
                    self.parsed_data.append([user, grav])
            else:
                self.parsed_data = parsed_samples
                
        except Exception as e:
            raise ValueError(f'Error parsing data: {str(e)}')