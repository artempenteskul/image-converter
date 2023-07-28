import os
import pika
import json

from PIL import Image

from utils import QualityEnum


UPLOAD_FOLDER = 'media'
IMG_CONVERTER_QUEUE = 'img-converter-queue'


def make_different_qualities_img(file_id: str, filename: str) -> None:
    for img_quality in (QualityEnum.SEVENTY_FIVE.value, QualityEnum.FIFTY.value, QualityEnum.TWENTY_FIVE.value):
        os.makedirs(os.path.join(UPLOAD_FOLDER, img_quality, file_id))
        with Image.open(os.path.join(UPLOAD_FOLDER, QualityEnum.HUNDRED.value, file_id, filename)) as img:
            img.save(os.path.join(UPLOAD_FOLDER, img_quality, file_id, filename), quality=int(img_quality))


def process_message(ch, method, properties, body):
    body = json.loads(body)
    file_id = body['file_id']
    filename = body['filename']
    make_different_qualities_img(file_id=file_id, filename=filename)
    print(f'File with file_id {file_id} and filename {filename} was successfully converted.')


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=IMG_CONVERTER_QUEUE)
    channel.basic_consume(queue=IMG_CONVERTER_QUEUE, on_message_callback=process_message, auto_ack=True)

    print('Waiting for messages. Process has started.')

    channel.start_consuming()
