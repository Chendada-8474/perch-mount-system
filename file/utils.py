import base64
import PIL.Image
import io


def encode(phrase: str) -> str:
    return


def read_byte_image(path: str) -> io.BytesIO:
    image_io = io.BytesIO()
    image = PIL.Image.open(path)
    image.thumbnail((960, 540))
    image.save(image_io, "JPEG")
    image_io.seek(0)
    return image_io
