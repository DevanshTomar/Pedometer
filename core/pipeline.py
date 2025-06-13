from .parser import Parser
from .processor import Processor
from .analyzer import Analyzer

class Pipeline:
    """Orchestrate the complete pedometer processing pipeline"""
    
    def __init__(self, data, user, trial):
        self.data = data
        self.user = user
        self.trial = trial
        self.parser = None
        self.processor = None
        self.analyzer = None
    
    @classmethod
    def run(cls, data, user, trial):
        pipeline = cls(data, user, trial)
        pipeline.feed()
        return pipeline
    
    def feed(self):
        """Run data through the complete pipeline"""
        self.parser = Parser.run(self.data)
        self.processor = Processor.run(self.parser.parsed_data)
        self.analyzer = Analyzer.run(self.processor.filtered_data, self.user, self.trial)