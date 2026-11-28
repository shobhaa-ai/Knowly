from src.knowly.vectorstore.search import semantic_search


def main():

    query = input("Enter your question: ")

    results = semantic_search(
        query=query,
        top_k=5,
    )

    print("\nSearch Results")
    print("=" * 60)

    if not results:
        print("No matching chunks found.")
        return

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Metadata: {result['metadata']}")
        print(f"Content:\n{result['content']}")


if __name__ == "__main__":
    main()