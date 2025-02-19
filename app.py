from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from color_extractor import extract_colors, get_palette_image, rgb_to_hex, save_palette_image
import os
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        colors = extract_colors(filepath, num_colors=5)
        palette = get_palette_image(colors, swatch_size=50)
        hex_codes = [rgb_to_hex(color) for color in colors]

        palette_path = os.path.join(app.config['UPLOAD_FOLDER'], 'palette.png')
        palette.save(palette_path)

        return render_template('result.html', hex_codes=hex_codes, palette_path='uploads/palette.png')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
