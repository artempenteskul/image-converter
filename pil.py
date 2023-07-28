import os

from PIL import Image

from utils import QualityEnum


UPLOAD_FOLDER = 'media'


def make_img_copies_with_different_qualities(file_id: str, filename: str) -> None:
    for img_quality in (QualityEnum.SEVENTY_FIVE.value, QualityEnum.FIFTY.value, QualityEnum.TWENTY_FIVE.value):
        with Image.open(os.path.join(UPLOAD_FOLDER, QualityEnum.HUNDRED.value, file_id, filename)) as img:
            img.save(os.path.join(UPLOAD_FOLDER, img_quality, filename), quality=int(img_quality))


# if __name__ == '__main__':
#     if not os.path.exists('media/75/111/'):
#         os.makedirs('media/75/111/')
#
#     if not os.path.exists('media/50/111/'):
#         os.makedirs('media/50/111/')
#
#     if not os.path.exists('media/25/111/'):
#         os.makedirs('media/25/111/')
#
#     reduce_image_quality('media/100/111/filename.jpg', 'media/75/111/filename.jpg', quality=75)
#     reduce_image_quality('media/100/111/filename.jpg', 'media/50/111/filename.jpg', quality=50)
#     reduce_image_quality('media/100/111/filename.jpg', 'media/25/111/filename.jpg', quality=25)
