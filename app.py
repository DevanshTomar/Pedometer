from flask import Flask, render_template, request, redirect, url_for, flash
import os
from utils.file_handler import Upload
from core.pipeline import Pipeline
from utils.data_generator import generate_example_data, create_plot

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
@app.route('/uploads')
def uploads():
    error = request.args.get('error')
    if error:
        flash(f'A {error} error has occurred.', 'error')
    
    pipelines = []
    for upload in Upload.all():
        try:
            with open(upload.file_path, 'r') as f:
                data = f.read()
            pipeline = Pipeline.run(data, upload.user, upload.trial)
            pipelines.append({
                'file_path': upload.file_path,
                'trial_name': upload.trial.name,
                'steps': pipeline.analyzer.steps,
                'distance': f"{pipeline.analyzer.distance:.2f}" if pipeline.analyzer.distance else "N/A",
                'time': f"{pipeline.analyzer.time:.2f}s" if pipeline.analyzer.time else "N/A",
                'delta': pipeline.analyzer.delta if pipeline.analyzer.delta is not None else "N/A"
            })
        except Exception as e:
            print(f"Error processing {upload.file_path}: {str(e)}")
    
    return render_template('uploads.html', pipelines=pipelines)

@app.route('/upload/<path:file_path>')
def upload_detail(file_path):
    try:
        upload = Upload.find(file_path)
        with open(file_path, 'r') as f:
            data = f.read()
        
        pipeline = Pipeline.run(data, upload.user, upload.trial)
        
        # Create plots
        dot_product_plot = create_plot(pipeline.processor.dot_product_data, 
                                     'Acceleration after Dot Product')
        filtered_plot = create_plot(pipeline.processor.filtered_data, 
                                  'Acceleration after Filtering')
        
        result = {
            'trial_name': upload.trial.name,
            'gender': upload.user.gender or 'N/A',
            'height': upload.user.height or 'N/A',
            'stride': f"{upload.user.stride:.2f}" if upload.user.stride else 'N/A',
            'rate': upload.trial.rate or 'N/A',
            'actual_steps': upload.trial.steps if upload.trial.steps is not None else 'N/A',
            'calculated_steps': pipeline.analyzer.steps,
            'distance': f"{pipeline.analyzer.distance:.2f} units" if pipeline.analyzer.distance else "N/A",
            'time': f"{pipeline.analyzer.time:.2f} seconds" if pipeline.analyzer.time else "N/A",
            'delta': pipeline.analyzer.delta if pipeline.analyzer.delta is not None else "N/A",
            'dot_product_plot': dot_product_plot,
            'filtered_plot': filtered_plot
        }
        
        return render_template('upload_detail.html', result=result)
    
    except Exception as e:
        flash(f'Error loading upload: {str(e)}', 'error')
        return redirect(url_for('uploads'))

@app.route('/create', methods=['POST'])
def create():
    try:
        if 'data' not in request.files:
            raise ValueError('No file uploaded')
        
        file = request.files['data']
        if file.filename == '':
            raise ValueError('No file selected')
        
        user_params = {
            'gender': request.form.get('gender'),
            'height': request.form.get('height'),
            'stride': request.form.get('stride')
        }
        
        trial_params = {
            'name': request.form.get('name'),
            'rate': request.form.get('rate'),
            'steps': request.form.get('steps')
        }
        
        Upload.create(file, user_params, trial_params)
        flash('Upload successful!', 'success')
        return redirect(url_for('uploads'))
    
    except Exception as e:
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('uploads', error='creation'))

if __name__ == '__main__':
    # Create example data on first run
    os.makedirs('example_data', exist_ok=True)
    if not os.path.exists('example_data/walking_data.txt'):
        with open('example_data/walking_data.txt', 'w') as f:
            f.write(generate_example_data())
    
    print("Pedometer application is ready!")
    print("Example data file created at: example_data/walking_data.txt")
    print("Starting Flask server...")
    
    app.run(debug=True, port=5000)