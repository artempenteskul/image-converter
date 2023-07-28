import pika


IMG_CONVERTER_QUEUE = 'img-converter-queue'


def process_message(ch, method, properties, body):
    print(f'Received: {body}')
    file_id_to_convert = body.decode('UTF-8')
    print(f'{file_id_to_convert}')


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='img-converter-queue')
    channel.basic_consume(queue='img-converter-queue', on_message_callback=process_message, auto_ack=True)

    print('Waiting for messages. Process has started.')

    channel.start_consuming()
