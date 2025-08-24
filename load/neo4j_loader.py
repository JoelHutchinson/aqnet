from neo4j import GraphDatabase

class Neo4jLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        props = ", ".join(f"{k}: ${k}" for k in properties.keys())
        query = f"MERGE (n:{label} {{{props}}})"
        with self.driver.session() as session:
            session.run(query, **properties)

    def create_relationship(self, source_label, source_key, source_val,
                            target_label, target_key, target_val, rel_type):
        query = (
            f"MATCH (a:{source_label} {{ {source_key}: $source_val }}), "
            f"(b:{target_label} {{ {target_key}: $target_val }}) "
            f"MERGE (a)-[:{rel_type}]->(b)"
        )
        with self.driver.session() as session:
            session.run(query, source_val=source_val, target_val=target_val)
