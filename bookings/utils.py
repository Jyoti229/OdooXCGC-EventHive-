import qrcode
from django.conf import settings
import os

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    media_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(media_path, exist_ok=True)
    file_path = os.path.join(media_path, filename)
    img.save(file_path)
    return 'qr_codes/' + filename
