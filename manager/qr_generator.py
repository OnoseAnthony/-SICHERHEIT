import qrcode

def generate_qrcode(qrdata):
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_code.add_data(qrdata)
    qr_code.make(fit=True)

    qr_image = qr_code.make_image(fill_color="black", back_color="white")

    return qr_image
