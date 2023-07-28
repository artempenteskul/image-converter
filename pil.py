# import os
#
# from PIL import Image
#
# from utils import QualityEnum
#
#
# UPLOAD_FOLDER = 'media'
#
#
# def make_different_qualities_img(file_id: str, filename: str) -> None:
#     for img_quality in (QualityEnum.SEVENTY_FIVE.value, QualityEnum.FIFTY.value, QualityEnum.TWENTY_FIVE.value):
#         os.makedirs(os.path.join(UPLOAD_FOLDER, img_quality, file_id))
#         with Image.open(os.path.join(UPLOAD_FOLDER, QualityEnum.HUNDRED.value, file_id, filename)) as img:
#             img.save(os.path.join(UPLOAD_FOLDER, img_quality, filename), quality=int(img_quality))
