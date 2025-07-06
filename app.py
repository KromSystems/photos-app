from flask import Flask, request, jsonify, send_file, abort
from io import BytesIO
from db import db
from config import config
from PIL import Image
import imghdr

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Валидация и обработка изображений
ALLOWED_MIME_TYPES = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'webp': 'image/webp'
}

def validate_image(image_data):
    """Проверяет валидность изображения"""
    # Определяем тип изображения по содержимому
    image_type = imghdr.what(None, h=image_data)
    if not image_type or image_type.lower() not in ALLOWED_MIME_TYPES:
        return None
    
    # Проверяем минимальный размер
    if len(image_data) < 4:
        return None
    
    # Проверяем максимальный размер
    if len(image_data) > config.MAX_CONTENT_LENGTH:
        return None
    
    return ALLOWED_MIME_TYPES[image_type.lower()]

@app.route('/photos', methods=['POST'])
def upload_photo():
    """Загрузка нового фото"""
    # Проверяем наличие файла в запросе
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Проверяем что файл не пустой
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Читаем данные файла
    image_data = file.read()
    
    # Валидируем изображение
    mime_type = validate_image(image_data)
    if not mime_type:
        return jsonify({'error': 'Invalid image format or size'}), 400
    
    # Сохраняем в базу данных
    try:
        result = db.save_photo(file.filename, image_data, mime_type)
        return jsonify({
            'message': 'Photo uploaded successfully',
            'photo_id': result['photo_id'],
            'file_size': result['file_size'],
            'created_at': result['created_at'].isoformat()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/photos/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    """Получение метаданных фото"""
    try:
        photo = db.get_photo(photo_id)
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        return jsonify({
            'photo_id': photo_id,
            'file_name': photo['file_name'],
            'mime_type': photo['mime_type'],
            'size': len(photo['image_data'])
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/photos/<int:photo_id>/image', methods=['GET'])
def get_photo_image(photo_id):
    """Получение самого изображения"""
    try:
        photo = db.get_photo(photo_id)
        if not photo:
            abort(404)
        
        # Создаем in-memory файл
        img_io = BytesIO(photo['image_data'])
        return send_file(
            img_io,
            mimetype=photo['mime_type'],
            as_attachment=False,
            download_name=photo['file_name']
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)