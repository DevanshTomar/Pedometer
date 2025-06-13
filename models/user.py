import config

class User:
    """User model with stride calculation"""
    
    def __init__(self, gender=None, height=None, stride=None):
        self.gender = None
        self.height = None
        self.stride = None
        
        if gender and gender.lower() in config.GENDER_OPTIONS:
            self.gender = gender.lower()
        elif gender and str(gender).strip():
            raise ValueError('Invalid gender')
        
        if height and str(height).strip():
            try:
                self.height = float(height)
                if self.height <= 0:
                    raise ValueError('Invalid height')
            except ValueError:
                if str(height).strip():
                    raise ValueError(f'Invalid height: {height}')
        
        if stride and str(stride).strip():
            try:
                self.stride = float(stride)
                if self.stride <= 0:
                    raise ValueError('Invalid stride')
            except ValueError:
                if str(stride).strip():
                    raise ValueError(f'Invalid stride: {stride}')
        else:
            self.stride = self._calculate_stride()
    
    def _calculate_stride(self):
        """Calculate stride based on available information"""
        if self.gender and self.height:
            return config.STRIDE_MULTIPLIERS[self.gender] * self.height
        elif self.height:
            avg_multiplier = sum(config.STRIDE_MULTIPLIERS.values()) / len(config.STRIDE_MULTIPLIERS)
            return avg_multiplier * self.height
        elif self.gender:
            return config.AVERAGE_STRIDES[self.gender]
        else:
            return sum(config.AVERAGE_STRIDES.values()) / len(config.AVERAGE_STRIDES)