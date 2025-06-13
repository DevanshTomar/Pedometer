from .filters import Filter

class Processor:
    """Process parsed data through filters and transformations"""
    
    def __init__(self, data):
        self.data = data
        self.dot_product_data = None
        self.filtered_data = None
    
    @classmethod
    def run(cls, data):
        processor = cls(data)
        processor.dot_product()
        processor.filter()
        return processor
    
    def dot_product(self):
        """Calculate dot product of user and gravitational acceleration"""
        self.dot_product_data = []
        for sample in self.data:
            user_accel = sample[0]
            grav_accel = sample[1]
            dot_prod = (user_accel[0] * grav_accel[0] + 
                       user_accel[1] * grav_accel[1] + 
                       user_accel[2] * grav_accel[2])
            self.dot_product_data.append(dot_prod)
    
    def filter(self):
        """Apply low-pass and high-pass filters"""
        self.filtered_data = Filter.low_5_hz(self.dot_product_data)
        self.filtered_data = Filter.high_1_hz(self.filtered_data)