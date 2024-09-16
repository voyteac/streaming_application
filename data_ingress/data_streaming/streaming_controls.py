from django.shortcuts import redirect

import threading
import logging

from data_ingress.kafka.kafka_container_control import kafka_container_check
from data_ingress.tcp_operations.tcp_server import start_data_flow
from data_ingress.data_streaming.streaming_controls_helper import start_thread

logger = logging.getLogger('streaming_app')
stop_streaming_flag = threading.Event()
streaming_thread = None


def start_data_collection(request):
    logger.info(f'{start_data_collection.__name__} -> Starting data collection.')
    global streaming_thread, stop_streaming_flag
    stop_streaming_flag.clear()
    is_kafka_container_running = kafka_container_check()
    if is_kafka_container_running or not streaming_thread or not streaming_thread.is_alive():

        streaming_thread = start_thread(start_data_flow, (stop_streaming_flag,), 'streaming')

        logger.info(f'{start_data_collection.__name__} -> Data collection started!')
        request.session['tcp_server_status'] = 'started'
    else:
        logger.error(f'{start_data_collection.__name__} -> '
                     f'Cannot start data collection is not running due to kafka_container_running: '
                     f'{is_kafka_container_running}')

        request.session['tcp_server_status'] = 'stopped'
    return redirect('control-panel')


def stop_data_collection(request):
    logger.info(f'{stop_data_collection.__name__} -> Stopping data collection')
    global stop_streaming_flag
    stop_streaming_flag.set()
    if streaming_thread and streaming_thread.is_alive():
        streaming_thread.join()
    logger.info(f'{stop_data_collection.__name__} -> Data collection stopped')
    request.session['tcp_server_status'] = 'stopped'
    return redirect('control-panel')
