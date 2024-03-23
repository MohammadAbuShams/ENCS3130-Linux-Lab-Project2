from library_management_system import LibraryManagementSystem

# Main program loop
lms = LibraryManagementSystem()

file_name = "lms_data.txt"
lms.load_books_from_file("lms_data.txt")

while True:
    print("\nLibrary Management System")
    print("1. Add new books to the library collection")
    print("2. Search for books within the library collection")
    print("3. Edit the information of existing books")
    print("4. Archive books")
    print("5. Remove books from the LMS")
    print("6. Generate reports about the books available in the LMS")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == '1':
        file_name = input("Enter the name of the file: ")
        lms.load_books_from_file(file_name)

    elif choice == '2':
        lms.search_books()
    elif choice == '3':
        lms.edit_book()
    elif choice == '4':
        lms.archive_book()
    elif choice == '5':
        lms.remove_book()

    elif choice == '6':
        lms.generate_reports()

    elif choice == '7':
        lms.exit_system()

    else:
        print("Invalid choice. Please try again.")
