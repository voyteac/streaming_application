from typing import Dict, Any

### DOCKER ###

wsl_docker_host: str = 'localhost'
wsl_docker_port: str = '2375'

### docker-compose commands kafka ###
kafka_docker_compose_path: str = '/mnt/c/Projects/streaming_app/streaming_app/scripts/kafka-docker'
kafka_docker_compose_up_wsl_cmd: str =  f'wsl -e bash -c "cd {kafka_docker_compose_path} && docker-compose up -d"'
kafka_docker_compose_down_wsl_cmd: str = f'wsl -e bash -c "cd {kafka_docker_compose_path} && docker-compose down"'


### docker-compose commands postgres ###
postgres_docker_compose_path: str = '/mnt/c/Projects/streaming_app/streaming_app/scripts/postgres'
postgres_docker_compose_up_wsl_cmd: str =  f'wsl -e bash -c "cd {postgres_docker_compose_path} && docker-compose up -d"'
postgres_docker_compose_down_wsl_cmd: str = f'wsl -e bash -c "cd {postgres_docker_compose_path} && docker-compose down"'


### docker-compose commands elk ###
elk_docker_compose_path: str = '/mnt/c/Projects/streaming_app/streaming_app/scripts/elk'
elk_docker_compose_up_wsl_cmd: str =  f'wsl -e bash -c "cd {elk_docker_compose_path} && docker-compose up -d"'
elk_docker_compose_down_wsl_cmd: str = f'wsl -e bash -c "cd {elk_docker_compose_path} && docker-compose down"'



### KAFKA Container ###
kafka_service_data: Dict [str, Any] = {
    'service_info': {
        'name': 'kafka'
    },
    'containers': [
        {
            'name': 'kafka'
        },
        {
            'name': 'zookeeper'
        }
    ],
    'session': {
        'storage_key': 'kafka_docker_service_status',
        'status_started': 'started',
        'status_stopped': 'stopped'
        },
    'redirect': {
        'pattern': 'data-ingress'
    },
    'ui_message': {
        'service_up': 'Kafka docker service is running!',
        'service_down': 'Kafka docker service is NOT running!'
    },

}


### ELK Containers ###
elk_service_data: Dict [str, Any] = {
    'service_info': {
        'name': 'ELK'
    },
    'containers': [
        {
            'name': 'elk_setup'
        },
        {
            'name': 'es01'
        },
        {
            'name': 'kibana'
        },
        {
            'name': 'logstash'
        }
    ],
    'session': {
        'storage_key': 'elk_docker_service_status',
        'status_started': 'started',
        'status_stopped': 'stopped'
        },
    'redirect': {
        'pattern': 'data-ingress'
    },
    'ui_message': {
        'service_up': 'ELK docker service is running!',
        'service_down': 'Kafka docker service is NOT running!'
    },
}

### PostgreSQL Container ###
postgres_service_data: Dict [str, Any] = {
    'service_info': {
        'name': 'postgres'
    },
    'containers': [
        {
            'name': 'postgresql'
        },
    ],
    'session': {
        'storage_key': 'postgres_docker_service_status',
        'status_started': 'started',
        'status_stopped': 'stopped'
        },
    'redirect': {
        'pattern': 'data-ingress'
    },
    'ui_message': {
        'service_up': 'PostgreSQL docker service is running!',
        'service_down': 'PostgreSQL docker service is NOT running!'
    },
}


data_collection: Dict [str, Any] = {
    'session': {
        'status_started': 'started',
        'status_stopped': 'stopped'
    },
    'ui_message': {
        'storage_key': 'data_collection_status',
        'service_up': 'Data Collection is started!',
        'service_down': 'Data Collection is NOT started!'
    },
    'redirect': {
        'pattern': 'data-ingress'
    }
}

data_generation: Dict [str, Any] = {
    'session': {
        'status_started': 'started',
        'status_stopped': 'stopped'
    },
    'ui_message': {
        'storage_key': 'data_generation_status',
        'service_up': 'Streaming is started!',
        'service_down': 'Streaming is NOT started!'
    },
    'redirect': {
        'pattern': 'data-ingress'
    }
}
