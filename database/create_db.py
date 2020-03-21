from py2neo import Graph, Node, Relationship

graph = Graph(password="admin")


def remove_all():
    transaction = "MATCH (n) DETACH DELETE n"
    graph.run(transaction)


if __name__ == "__main__":
    with open("spo.jl") as f:
        spos = [eval(line.strip()) for line in f.readlines()]
    remove_all()
    for spo in spos:
        subj, rel, obj = spo.values()
        transaction = (
            f"MERGE (a:Person {{name: '{subj}'}})\n"
            + f"MERGE (b:Person {{name: '{obj}'}})\n"
            + f"CREATE (a) -[:{rel}]-> (b) "
        )
        print(transaction)
        graph.run(transaction)
