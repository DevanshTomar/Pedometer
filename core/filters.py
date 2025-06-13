import config

class Filter:
    """IIR Filter implementation for signal processing"""
    
    @classmethod
    def low_0_hz(cls, data):
        """Low-pass filter for extracting gravitational acceleration"""
        return cls._filter(data, config.COEFFICIENTS_LOW_0_HZ)
    
    @classmethod
    def low_5_hz(cls, data):
        """Low-pass filter for removing high-frequency noise"""
        return cls._filter(data, config.COEFFICIENTS_LOW_5_HZ)
    
    @classmethod
    def high_1_hz(cls, data):
        """High-pass filter for removing low-frequency drift"""
        return cls._filter(data, config.COEFFICIENTS_HIGH_1_HZ)
    
    @classmethod
    def _filter(cls, data, coefficients):
        """Apply IIR filter with given coefficients"""
        filtered_data = [0, 0]
        
        for i in range(2, len(data)):
            filtered_value = coefficients['alpha'][0] * (
                data[i] * coefficients['beta'][0] +
                data[i-1] * coefficients['beta'][1] +
                data[i-2] * coefficients['beta'][2] -
                filtered_data[i-1] * coefficients['alpha'][1] -
                filtered_data[i-2] * coefficients['alpha'][2]
            )
            filtered_data.append(filtered_value)
        
        return filtered_data