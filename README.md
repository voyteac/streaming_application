# streaming_app

Streaming application.

Three options:
1. Data Ingress 
<br />1.1. Generation
<br />1.2. Data Collection
<br />1.3. Dokcer Service Control - Kafka, ELK and PostrgreSQL (read-only)
<br />1.4. Clean database
2. Data Display - quick PostgreSQL reader
3. Data Analysis - check metric patterns and for metric 0 check anomalies

Flow:

0. Start app.
1. Start Kafka.
2. Start ELK.
3. Start Data Collection.
4. Define number of clients, and start Data Generation.
5. Check data in Data Display view - quick preview.
6. Check KPI value in Data Analysis.
7. Open Kibana for more advanced analysis.


For high level view please check "overview.graphml".
Editor -> yEd.

Used technologies:
1. Django web framework.
2. Google Protocol Buffers.
3. TCP Streams + Google Protobuf.
4. Kafka.
5. Docker.
6. Postgresql.
7. ELK