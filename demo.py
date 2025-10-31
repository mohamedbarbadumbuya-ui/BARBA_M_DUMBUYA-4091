# demo.py
from Operations import Library, GENRES, LibraryError

def pretty_print_book(b):
    print(f"{b['isbn']}: {b['title']} by {b['author']} ({b['genre']}) copies:{b['total_copies']} borrowed:{b['borrowed_count']}")

def run_demo():
    lib = Library()

    print("=== DEMO: create books and members ===")
    lib.add_book("978-0001", "The Little Prince", "Antoine de Saint-Exupéry", "Fiction", total_copies=2)
    lib.add_book("978-0002", "A Brief History of Time", "Stephen Hawking", "Non-Fiction", total_copies=1)

    lib.add_member("M001", "Alice", "alice@example.com")
    lib.add_member("M002", "Bob", "bob@example.com")

    print("\nBooks after adding:")
    for b in lib.search_books():
        pretty_print_book(b)

    print("\nAlice borrows The Little Prince")
    try:
        lib.borrow_book("M001", "978-0001")
    except LibraryError as e:
        print("Error:", e)
    print("Alice info:", lib.member_info("M001"))

    print("\nBob tries to borrow A Brief History of Time")
    lib.borrow_book("M002", "978-0002")
    print("Bob info:", lib.member_info("M002"))

    print("\nAttempting to delete book that has borrowed copies (should fail):")
    try:
        lib.delete_book("978-0002")
    except LibraryError as e:
        print("Expected error:", e)

    print("\nBob returns A Brief History of Time")
    lib.return_book("M002", "978-0002")
    print("Bob info:", lib.member_info("M002"))

    print("\nNow delete book 978-0002 (should succeed):")
    lib.delete_book("978-0002")
    print("Books now:")
    for b in lib.search_books():
        pretty_print_book(b)

if __name__ == "__main__":
    run_demo()
