from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def encrypt_image(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j][:3]
            pixels[i, j] = ((r + 50) % 256, (g + 100) % 256, (b + 150) % 256)
    encrypted_path = os.path.join(UPLOAD_FOLDER, "encrypted.png")
    img.save(encrypted_path)
    return encrypted_path


def decrypt_image(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j][:3]
            pixels[i, j] = ((r - 50) % 256, (g - 100) % 256, (b - 150) % 256)
    decrypted_path = os.path.join(UPLOAD_FOLDER, "decrypted.png")
    img.save(decrypted_path)
    return decrypted_path


@app.route('/', methods=['GET', 'POST'])
def index():
    original_img = encrypted_img = decrypted_img = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            original_path = os.path.join(UPLOAD_FOLDER, "original.png")
            file.save(original_path)

            encrypted_path = encrypt_image(original_path)
            decrypted_path = decrypt_image(encrypted_path)

            return render_template("index.html",
                                   original=original_path,
                                   encrypted=encrypted_path,
                                   decrypted=decrypted_path)
    return render_template("index.html")


@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
