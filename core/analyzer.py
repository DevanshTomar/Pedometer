import config

class Analyzer:
    """Analyze processed data to count steps and calculate metrics"""
    
    def __init__(self, data, user, trial):
        self.data = data
        self.user = user
        self.trial = trial
        self.steps = 0
        self.delta = None
        self.distance = None
        self.time = None
    
    @classmethod
    def run(cls, data, user, trial):
        analyzer = cls(data, user, trial)
        analyzer.measure_steps()
        analyzer.measure_delta()
        analyzer.measure_distance()
        analyzer.measure_time()
        return analyzer
    
    def measure_steps(self):
        """Count steps using threshold crossing with hysteresis"""
        self.steps = 0
        count_steps = True
        
        for i in range(1, len(self.data)):
            # Check for positive threshold crossing
            if self.data[i] >= config.STEP_THRESHOLD and self.data[i-1] < config.STEP_THRESHOLD:
                if count_steps:
                    self.steps += 1
                    count_steps = False
            
            # Check for negative zero crossing (hysteresis)
            if self.data[i] < 0 and self.data[i-1] >= 0:
                count_steps = True
    
    def measure_delta(self):
        """Calculate difference between measured and actual steps"""
        if self.trial.steps is not None:
            self.delta = self.steps - self.trial.steps
    
    def measure_distance(self):
        """Calculate distance traveled"""
        self.distance = self.user.stride * self.steps
    
    def measure_time(self):
        """Calculate elapsed time"""
        if self.trial.rate:
            self.time = len(self.data) / self.trial.rate