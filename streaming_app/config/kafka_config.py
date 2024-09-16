bootstrap_servers = 'localhost:9092'
api_version = (0, 10, 1)
topic_name = 'test'
kafka_container_name = 'kafka'
zookeeper_container_name = 'zookeeper'
kafka_container_up_status = 'kafka: Up'
zookeeper_container_up_status = 'zookeeper: Up'

zookeeper_host = "localhost"
zookeeper_port = 2181
zookeeper_set_max_retries = 10
zookeeper_launch_retry_timer = 3

docker_compose_path = '/mnt/c/Projects/streaming_app/streaming_app/scripts/kafka-docker'
wsl_command_zookeeper = f'wsl -e bash -c "cd {docker_compose_path} && docker-compose up -d zookeeper"'
wsl_command_kafka = f'wsl -e bash -c "cd {docker_compose_path} && docker-compose up -d kafka"'

wsl_command_kafka_stop = f'wsl -e bash -c "cd {docker_compose_path} && docker-compose down"'

wsl_command_to_get_container_status = 'wsl bash -c "docker ps -a --format \\"{{.Names}}: {{.Status}}\\""'

wsl_confirm_kafka_stopped = 'Removing kafka     ... done'