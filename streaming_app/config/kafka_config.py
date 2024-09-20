from typing import Tuple

bootstrap_servers: str = 'localhost:9092'
producer_api_version: Tuple[int, int, int] = (0, 10, 1)
consumer_api_version: Tuple[int, int, int] = (0, 10, 1)

odd_client_id_topic_name: str = 'odd_client_id_topic'
even_client_id_topic_name: str = 'even_client_id_topic'

kafka_container_name: str = 'kafka'
zookeeper_container_name: str = 'zookeeper'
kafka_container_up_status: str = 'kafka: Up'
zookeeper_container_up_status: str = 'zookeeper: Up'

zookeeper_host: str = "localhost"
zookeeper_port: int = 2181
zookeeper_set_max_retries: int = 10
zookeeper_launch_retry_timer: int = 3

docker_compose_path: str = '/mnt/c/Projects/streaming_app/streaming_app/scripts/kafka-docker'
wsl_command_zookeeper_start: str = f'wsl -e bash -c "cd {docker_compose_path} && docker-compose up -d zookeeper"'
wsl_command_kafka_start: str = f'wsl -e bash -c "cd {docker_compose_path} && docker-compose up -d kafka"'

wsl_command_kafka_stop: str = f'wsl -e bash -c "cd {docker_compose_path} && docker-compose down"'

wsl_command_to_get_container_status: str = 'wsl bash -c "docker ps -a --format \\"{{.Names}}: {{.Status}}\\""'

wsl_confirm__string_kafka_stopped: str = 'Removing kafka     ... done'