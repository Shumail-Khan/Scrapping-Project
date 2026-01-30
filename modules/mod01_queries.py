# modules/01_queries.py

def get_queries():
    """
    Dynamically collect queries from the user at runtime
    """
    queries = []
    print("Enter queries (press ENTER without text to stop):")

    counter = 1
    while True:
        q = input(f"Query {counter}: ").strip()
        if not q:
            break
        queries.append({
            "query_id": f"Q{counter}",
            "query_text": q
        })
        counter += 1

    return queries