import csv

from neo4j import GraphDatabase

from config_loader import get_configs


class Neo4jService:
    __domain = get_configs()['neo4j']['node-label']

    def __init__(self):
        self.__uri = get_configs()['neo4j']['uri']
        self.__username = get_configs()['neo4j']['username']
        self.__password = get_configs()['neo4j']['password']
        self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__username, self.__password))
        self.__session = self.__driver.session()

    def get_edges_with_ids(self):
        return self.__session.run(
            f"MATCH (predecessor_url: {self.__domain})"
            f"-[r:LINKED_TO]->"
            f"(successor_url:{self.__domain}) "
            f"RETURN ID(predecessor_url), ID(successor_url)")

    def get_nodes_with_ids(self):
        return self.__session.run(
            f"MATCH(url: {self.__domain}) "
            f"RETURN url.url, ID(url) "
            f"ORDER BY url.url"
        )

    def run_statement(self, statement):
        self.__session.run(statement)


def write_edges_to_file(neo4j_service_obj, file_path):
    with open(file_path, 'w', newline='') as edge_numbered_file:
        edges = neo4j_service_obj.get_edges_with_ids()
        pairs_numbered_writer = csv.writer(edge_numbered_file, delimiter='\t')
        for edge in edges:
            pair = [edge['ID(predecessor_url)'], edge['ID(successor_url)']]
            pairs_numbered_writer.writerow(pair)


def write_node_numbered(neo4j_service_obj, file_path):
    with open(file_path, 'w', newline='') as nodes_numbered_file:
        node_numbered_writer = csv.writer(nodes_numbered_file, delimiter=',')
        nodes = neo4j_service_obj.get_nodes_with_ids()
        for node in nodes:
            node_numbered_writer.writerow([node[f"url.url"],
                                           node[f"ID(url)"]])


if __name__ == '__main__':
    neo4j_service_instance = Neo4jService()
    write_edges_to_file(neo4j_service_instance, f'{get_configs()["neo4j"]["node-label"]}_edges_numbered.csv')
    write_node_numbered(neo4j_service_instance, f'{get_configs()["neo4j"]["node-label"]}_nodes_numbered.csv')
