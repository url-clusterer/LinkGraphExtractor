from kafka import KafkaProducer

from config_loader import get_configs


class LinkGraphPipeline(object):
    __neo4j_node_label = get_configs()['neo4j']['node-label']
    __bootstrap_servers = get_configs()['kafka']['bootstrap-servers']
    __topic = get_configs()['kafka']['topic']
    __kafka_producer = KafkaProducer(bootstrap_servers=__bootstrap_servers)

    def get_kafka_message(self, predecessor_url, successor_url):
        return str.encode(f"MERGE (predecessor_url: {self.__neo4j_node_label} {{url: \"{predecessor_url}\"}}) "
                          f"MERGE (successor_url: {self.__neo4j_node_label} {{url: \"{successor_url}\"}}) "
                          f"MERGE (predecessor_url)-[r: LINKED_TO]->(successor_url)")

    def process_item(self, item, spider):
        successor_urls = []
        for successor_url in item['successor_urls']:
            successor_urls.append(successor_url)
            message = self.get_kafka_message(item['predecessor_url'], successor_url)
            self.__kafka_producer.send(self.__topic, message)
        return item
