import os
import qrcode
from dotenv import load_dotenv

load_dotenv()

def main():
    # take URL from .env and generate QR code
    url = os.getenv("URL")
    print(url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")

if __name__ == "__main__":
    main()