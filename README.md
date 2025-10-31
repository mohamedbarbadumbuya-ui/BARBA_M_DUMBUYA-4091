# BARBA_M_DUMBUYA-4091

## Mini Library Management System (PROG211 Assignment 1)

Files to submit:
- operations.py          (core functions)
- demo.py                (demo script that shows usage)
- tests.py               (unit tests using simple assert statements)
- UML.png / UML.pdf      (hand-drawn UML diagram scanned or photographed)
- DesignRationale.pdf    (1-2 page design rationale)
- README.md              (this file)

Requirements:
- Python 3.8+ (should work on 3.8, 3.9, 3.10+)

How to run:
1. Run the demo script:
   python demo.py

2. Run the tests:
   python tests.py
   (tests.py uses plain assert statements and prints "All tests passed." on success.)

Notes:
- GENRES are defined in operations.py; adjust or expand if you need other categories.
- exceptions of type LibraryError indicate constraint violations (duplicate ISBN, invalid genre, delete with borrowed copies, etc.)
