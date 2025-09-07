from load.neo4j_loader import Neo4jLoader
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_CONFIG = {
    "uri": os.getenv("NEO4J_URI"),
    "user": os.getenv("NEO4J_USER"),
    "password": os.getenv("NEO4J_PASSWORD")
}

loader = Neo4jLoader(**NEO4J_CONFIG)

with loader.driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) AS total_nodes")
    total_nodes = result.single()["total_nodes"]
    print(f"Total nodes in database: {total_nodes}")

loader.close()
