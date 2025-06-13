import os
import json
from datetime import datetime
import config
from models import User, Trial

class Upload:
    """Handle file uploads and metadata storage"""
    
    def __init__(self, file_path, user, trial):
        self.file_path = file_path
        self.user = user
        self.trial = trial
    
    @classmethod
    def create(cls, file, user_params, trial_params):
        """Create a new upload with metadata"""
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{trial_params['name']}_{timestamp}.txt"
        file_path = os.path.join(config.UPLOAD_FOLDER, filename)
        
        file.save(file_path)
        
        user = User(
            gender=user_params.get('gender'),
            height=user_params.get('height'),
            stride=user_params.get('stride')
        )
        
        trial = Trial(
            name=trial_params['name'],
            rate=trial_params.get('rate'),
            steps=trial_params.get('steps')
        )
        
        metadata = {
            'user': {
                'gender': user.gender,
                'height': user.height,
                'stride': user.stride
            },
            'trial': {
                'name': trial.name,
                'rate': trial.rate,
                'steps': trial.steps
            }
        }
        
        metadata_path = file_path.replace('.txt', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        return cls(file_path, user, trial)
    
    @classmethod
    def find(cls, file_path):
        """Find an upload by file path"""
        metadata_path = file_path.replace('.txt', '_metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        user = User(
            gender=metadata['user']['gender'],
            height=metadata['user']['height'],
            stride=metadata['user']['stride']
        )
        
        trial = Trial(
            name=metadata['trial']['name'],
            rate=metadata['trial']['rate'],
            steps=metadata['trial']['steps']
        )
        
        return cls(file_path, user, trial)
    
    @classmethod
    def all(cls):
        """Get all uploads"""
        uploads = []
        if os.path.exists(config.UPLOAD_FOLDER):
            for filename in os.listdir(config.UPLOAD_FOLDER):
                if filename.endswith('.txt'):
                    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
                    try:
                        upload = cls.find(file_path)
                        uploads.append(upload)
                    except:
                        pass
        return uploads