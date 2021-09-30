from PIL import Image, ImageOps
import mimetypes
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


def generate_thumbnail_crop(file, width, height):
    im = Image.open(file)
    if im.mode in ('RGBA', 'P'):
        im = im.convert('RGB')
    filename = file.name.split('/')[-1].split('.')[0]
    mime = mimetypes.guess_type(file.name)[0]
    file_type = mime.split('/')[-1]
    filename = filename + '-.' + file_type
    im = ImageOps.fit(im, (width, height), Image.ANTIALIAS)
    memory_file = BytesIO()
    im.save(memory_file, 'jpeg')
    suf = SimpleUploadedFile(
        filename, memory_file.getvalue(), content_type=mime)
    return suf
