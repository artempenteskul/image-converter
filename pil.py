import os

from PIL import Image


def reduce_image_quality(input_path, output_path, quality):
    with Image.open(input_path) as img:
        img.save(output_path, quality=quality)


if __name__ == '__main__':
    if not os.path.exists('media/75/111/'):
        os.makedirs('media/75/111/')

    if not os.path.exists('media/50/111/'):
        os.makedirs('media/50/111/')

    if not os.path.exists('media/25/111/'):
        os.makedirs('media/25/111/')

    reduce_image_quality('media/100/111/filename.jpg', 'media/75/111/filename.jpg', quality=75)
    reduce_image_quality('media/100/111/filename.jpg', 'media/50/111/filename.jpg', quality=50)
    reduce_image_quality('media/100/111/filename.jpg', 'media/25/111/filename.jpg', quality=25)
