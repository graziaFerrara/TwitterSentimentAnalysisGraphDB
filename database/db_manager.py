import neo4j, neomodel

class DBManager:

    def __init__(self, port, db_name, username, password):
        self._port = port
        self._db_name = db_name
        self._username = username
        self._password = password

        uri = f"bolt://localhost:{port}/{db_name}"
        driver = neo4j.GraphDatabase.driver(uri, auth=(username, password))
        neomodel.db.set_connection(uri, driver)

    def create_node(self, node):
        node.save()

    def create_index(self, index_name, node_type, property_name):
        neomodel.db.cypher_query(f"CREATE INDEX {index_name} IF NOT EXISTS FOR (n:{node_type}) ON (n.{property_name})")

    def create_compound_index(self, index_name, node_type, property_names):
        query = f"CREATE INDEX {index_name} IF NOT EXISTS FOR (n:{node_type}) ON ("
        for property_name in property_names:
            query += f"n.{property_name}, "
        query = query[:-2] + ")"
        neomodel.db.cypher_query(query)

    def delete_all(self):
        neomodel.db.cypher_query("MATCH (n) DETACH DELETE n")

    def get_all_nodes(self):
        return neomodel.db.cypher_query("MATCH (n) RETURN n")
    
    def get_all_relationships(self):
        return neomodel.db.cypher_query("MATCH ()-[r]->() RETURN r")
    
    def get_all_nodes_of_type(self, node_type):
        return neomodel.db.cypher_query(f"MATCH (n:{node_type}) RETURN n")
    
    def get_all_relationships_of_type(self, relationship_type):
        return neomodel.db.cypher_query(f"MATCH ()-[r:{relationship_type}]->() RETURN r")
    
    def get_all_nodes_and_relationships(self):
        return neomodel.db.cypher_query("MATCH (n)-[r]->(m) RETURN n, r, m")
    
    def get_all_nodes_and_relationships_of_type(self, node_type, relationship_type):
        return neomodel.db.cypher_query(f"MATCH (n:{node_type})-[r:{relationship_type}]->(m) RETURN n, r, m")

    def get_node_by_id(self, node_id):
        return neomodel.db.cypher_query(f"MATCH (n) WHERE ID(n) = {node_id} RETURN n")
    
    def get_node_by_property(self, node_type, property_name, property_value):
        return neomodel.db.cypher_query(f"MATCH (n:{node_type}) WHERE n.{property_name} = '{property_value}' RETURN n")
