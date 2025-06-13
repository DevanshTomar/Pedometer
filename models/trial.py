class Trial:
    """Trial model for storing walk metadata"""
    
    def __init__(self, name, rate=None, steps=None):
        self.name = name.replace(' ', '')
        if not self.name:
            raise ValueError('Invalid name')
        
        self.rate = None
        self.steps = None
        
        if rate and str(rate).strip():
            try:
                self.rate = int(rate)
                if self.rate <= 0:
                    raise ValueError('Invalid rate')
            except ValueError:
                if str(rate).strip():
                    raise ValueError(f'Invalid rate: {rate}')
        
        if steps is not None and str(steps).strip():
            try:
                self.steps = int(steps)
                if self.steps < 0:
                    raise ValueError('Invalid steps')
            except ValueError:
                if str(steps).strip():
                    raise ValueError(f'Invalid steps: {steps}')