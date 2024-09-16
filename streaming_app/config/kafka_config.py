bootstrap_servers = 'localhost:9092'
api_version = (0, 10, 1)
topic_name = 'test'
kafka_container_name = 'kafka'
zookeeper_container_name = 'zookeeper'
kafka_container_up_status = 'kafka: Up'
zookeeper_container_up_status = 'zookeeper: Up'

wsl_command_kafka_start = 'wsl bash /home/wjaroni/kafka-docker/kafka_start.sh'
wsl_command_kafka_stop = 'wsl bash /home/wjaroni/kafka-docker/kafka_stop.sh'
wsl_command_to_get_container_status = 'wsl bash -c "docker ps -a --format \\"{{.Names}}: {{.Status}}\\""'
