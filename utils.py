import os
import pika
import uuid

from enum import Enum


# TODO: move these hardcoded variables to the env variables / config files
UPLOAD_FOLDER = 'media'
IMG_CONVERTER_QUEUE = 'img-converter-queue'


class QualityEnum(Enum):
    HUNDRED = '100'
    SEVENTY_FIVE = '75'
    FIFTY = '50'
    TWENTY_FIVE = '25'


def generate_id_for_file() -> str:
    # TODO: check whether this uuid already exists in for our files (use listdir for check)
    return str(uuid.uuid4())


def get_filename_from_file_id(file_id: str) -> str:
    if os.path.exists(os.path.join(UPLOAD_FOLDER, QualityEnum.HUNDRED.value, file_id)):
        files_in_folder = os.listdir(os.path.join(UPLOAD_FOLDER, QualityEnum.HUNDRED.value, file_id))
        if len(files_in_folder) > 1:
            # TODO: add better explanation for exception here
            raise Exception('Multiple files for one id.')
        filename = files_in_folder[0]
        return filename
    else:
        # TODO: add better explanation for exception here
        raise Exception('Unknown files route.')


def send_message_to_rabbitmq(message):
    # TODO: extract connection to rabbitmq to env variables (localhost for example)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=IMG_CONVERTER_QUEUE)
    channel.basic_publish(exchange='', routing_key=IMG_CONVERTER_QUEUE, body=message)
    connection.close()
