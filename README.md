# streaming_app

Streaming application.

Three options:
1. Data Generation
2. Data Collection
3. Control Kafka Container

Flow:

0. Prerequisite: WSL must be lunched with Kafka container available and Postgresql installed and configured.
1. Start Kafka container.
2. Start Data Collection.
3. Define number of clients, and start data generation.

For high level view please check "overview.graphml".
Editor -> yEd.

Used technologies:
1. Django web framework.
2. Google Protocol Buffers.
3. TCP Streams.
4. Kafka.
5. Docker.
6. Postgresql.