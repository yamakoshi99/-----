from flask import Flask, render_template, request, jsonify
from gs1_utils import calculate_check_digit
import csv
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_single', methods=['POST'])
def calculate_single():
    data = request.form.get('code')
    if not data:
        return jsonify({'error': 'データが入力されていません'})
    result = calculate_check_digit(data)
    return jsonify({'result': result})

@app.route('/calculate_text', methods=['POST'])
def calculate_text():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'データが入力されていません'})
    
    results = []
    reader = csv.reader(text.splitlines())
    for row in reader:
        if row:
            data = row[0]
            check_digit = calculate_check_digit(data)
            results.append(f"{data}{check_digit}")
    
    return jsonify({'results': results})

@app.route('/calculate_file', methods=['POST'])
def calculate_file():
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルがアップロードされていません'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'})
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'CSVファイルのみ対応しています'})
    
    results = []
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    reader = csv.reader(stream)
    for row in reader:
        if row:
            data = row[0]
            check_digit = calculate_check_digit(data)
            results.append(f"{data}{check_digit}")
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
