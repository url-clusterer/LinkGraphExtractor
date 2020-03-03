from kafka import KafkaConsumer

from config_loader import get_configs
from neo4j_service import Neo4jService


class KafkaConsumerService:
    __neo4j_service = Neo4jService()
    __kafka_consumer = KafkaConsumer(get_configs()['kafka']['topic'],
                                     group_id=get_configs()['kafka']['group-id'],
                                     bootstrap_servers=get_configs()['kafka']['bootstrap-servers'])

    def consume_and_send(self):
        for message in self.__kafka_consumer:
            statement = message.value.decode()
            if statement is not None and statement:
                self.__neo4j_service.run_statement(statement)


def main():
    kafka_consumer_service = KafkaConsumerService()
    kafka_consumer_service.consume_and_send()


if __name__ == '__main__':
    main()
