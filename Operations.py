# operations.py
from typing import Dict, List, Optional

GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "History", "Children")

class LibraryError(Exception):
    pass

class Library:
    def __init__(self):
        self.books: Dict[str, Dict] = {}
        self.members: List[Dict] = []

    # ---------- Book operations ----------
    def add_book(self, isbn: str, title: str, author: str, genre: str, total_copies: int = 1) -> None:
        isbn = str(isbn)
        if isbn in self.books:
            raise LibraryError(f"Book with ISBN {isbn} already exists.")
        if genre not in GENRES:
            raise LibraryError(f"Genre '{genre}' is invalid. Valid genres: {GENRES}")
        if total_copies < 1:
            raise LibraryError("total_copies must be >= 1")
        self.books[isbn] = {
            "title": title,
            "author": author,
            "genre": genre,
            "total_copies": int(total_copies),
            "borrowed_count": 0
        }

    def update_book(self, isbn: str, **fields) -> None:
        isbn = str(isbn)
        if isbn not in self.books:
            raise LibraryError(f"No book with ISBN {isbn}.")
        book = self.books[isbn]
        if "genre" in fields and fields["genre"] not in GENRES:
            raise LibraryError(f"Genre '{fields['genre']}' is invalid.")
        # prevent decreasing total_copies below borrowed_count
        if "total_copies" in fields:
            new_total = int(fields["total_copies"])
            if new_total < book["borrowed_count"]:
                raise LibraryError("new total_copies cannot be less than borrowed_count")
            book["total_copies"] = new_total
        for key in ("title", "author", "genre"):
            if key in fields:
                book[key] = fields[key]

    def delete_book(self, isbn: str) -> None:
        isbn = str(isbn)
        if isbn not in self.books:
            raise LibraryError(f"No book with ISBN {isbn}.")
        book = self.books[isbn]
        if book["borrowed_count"] > 0:
            raise LibraryError("Cannot delete a book that has borrowed copies.")
        del self.books[isbn]

    def search_books(self, *, title: Optional[str] = None, author: Optional[str] = None) -> List[Dict]:
        results = []
        for isbn, book in self.books.items():
            if title and title.lower() not in book["title"].lower():
                continue
            if author and author.lower() not in book["author"].lower():
                continue
            entry = book.copy()
            entry["isbn"] = isbn
            results.append(entry)
        return results

    # ---------- Member operations ----------
    def add_member(self, member_id: str, name: str, email: str) -> None:
        if any(m["id"] == member_id for m in self.members):
            raise LibraryError(f"Member id {member_id} already exists.")
        self.members.append({"id": member_id, "name": name, "email": email, "borrowed_books": []})

    def update_member(self, member_id: str, **fields) -> None:
        m = self._find_member(member_id)
        if m is None:
            raise LibraryError(f"No member with id {member_id}")
        for k in ("name", "email"):
            if k in fields:
                m[k] = fields[k]

    def delete_member(self, member_id: str) -> None:
        m = self._find_member(member_id)
        if m is None:
            raise LibraryError(f"No member with id {member_id}")
        if m["borrowed_books"]:
            raise LibraryError("Cannot delete member with borrowed books.")
        self.members.remove(m)

    def _find_member(self, member_id: str) -> Optional[Dict]:
        for m in self.members:
            if m["id"] == member_id:
                return m
        return None

    # ---------- Borrow / Return ----------
    def borrow_book(self, member_id: str, isbn: str) -> None:
        isbn = str(isbn)
        m = self._find_member(member_id)
        if m is None:
            raise LibraryError("Member not found.")
        if isbn not in self.books:
            raise LibraryError("Book not found.")
        book = self.books[isbn]
        available = book["total_copies"] - book["borrowed_count"]
        if available <= 0:
            raise LibraryError("No copies available to borrow.")
        if len(m["borrowed_books"]) >= 3:
            raise LibraryError("Member has already borrowed maximum (3) books.")
        # all checks passed
        book["borrowed_count"] += 1
        m["borrowed_books"].append(isbn)

    def return_book(self, member_id: str, isbn: str) -> None:
        isbn = str(isbn)
        m = self._find_member(member_id)
        if m is None:
            raise LibraryError("Member not found.")
        if isbn not in m["borrowed_books"]:
            raise LibraryError("This member did not borrow that book.")
        book = self.books.get(isbn)
        if book is None:
            # book record missing: still remove from member but warn
            m["borrowed_books"].remove(isbn)
            raise LibraryError("Book record missing from library; removed from member record.")
        # normal return
        m["borrowed_books"].remove(isbn)
        book["borrowed_count"] -= 1

    # ---------- Helpers ----------
    def book_info(self, isbn: str) -> Dict:
        isbn = str(isbn)
        if isbn not in self.books:
            raise LibraryError("Book not found.")
        return {**self.books[isbn], "isbn": isbn}

    def member_info(self, member_id: str) -> Dict:
        m = self._find_member(member_id)
        if m is None:
            raise LibraryError("Member not found.")
        return m.copy()
