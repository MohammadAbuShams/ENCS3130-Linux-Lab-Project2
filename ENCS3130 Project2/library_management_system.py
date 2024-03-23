from book import Book


class LibraryManagementSystem:
    def __init__(self):
        self.books = []
        self.archive_books = []

    def add_book(self, book):
        existing_book = self.find_book_by_isbn(
            book.BookInfo["ISBN-10"], book.BookInfo["ISBN-13"])
        if existing_book != -1:
            print("A book with the same ISBN already exists in the library.")
            print("1. Replace existing record")
            print("2. Add another copy")
            choice = int(input("Enter your choice (1 or 2): "))
            if choice == 1:
                self.books.remove(self.books[existing_book])
                self.books.append(book)
                print("Book record replaced successfully.")
            elif choice == 2:
                self.books[existing_book].num_copies += 1
                print("Another copy of the book added successfully.")
                print(self.books[existing_book])
            else:
                print("Invalid choice. No changes made.")
        else:
            self.books.append(book)
            print("****************************************")
            print("Book added to the library successfully.")
            print("*****************************************")

    def find_book_by_isbn(self, isbn10, isbn13):
        # find the index of the book with the given isbn
        for i in range(len(self.books)):
            if self.books[i].BookInfo["ISBN-10"] == isbn10 and self.books[i].BookInfo["ISBN-13"] == isbn13:
                return i
        return -1

    def find_book_by_title(self, title):
        # find the index of the book with the given isbn
        for i in range(len(self.books)):
            if self.books[i].BookInfo["Title"].lower() == title.lower():
                return i
        return -1

    def load_books_from_file(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                book_info = {}
                print("Book information:")
                length = len(lines)
                counter = 0
                for line in lines:
                    counter += 1
                    line = line.strip()
                    if line:
                        line = line.replace('\u200f', '')
                        line = line.replace('\u200e', '')
                        key, value = line.split(' : ', 1)
                        book_info[key.strip()] = value.strip()
                    if counter == length or not line:
                        for key, value in book_info.items():
                            print(f"{key}: {value}")
                        # print("----------------------")
                        self.create_book_from_info(book_info)
                        book_info = {}
            print("Books loaded from file successfully.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print("An error occurred while loading books:", str(e))

    def create_book_from_info(self, book_info):
        book = Book(book_info)
        self.add_book(book)

    def search_books(self):
        print("Search for books:")
        key = input("Enter the key: ")
        search_results = []
        for book in self.books:
            for value in book.BookInfo.values():
                if key.strip().lower() == value.strip().lower():
                    search_results.append(book)

        if search_results:
            print("Search Results:")
            for book in search_results:
                print(book)
            print("----------------------")

            choice = input(
                "Do you want to store the results in a text file? (yes/no): ")
            if choice.lower() == "yes":
                file_name = input("Enter the file name: ")
                self.store_search_results(search_results, file_name)
                print("Search results stored successfully.")
        else:
            print("No matching books found.")

    def edit_book(self):
        print("Edit book:")
        print("Enter the method you prefer to search: ")
        print("1. ISBN")
        print("2. Title")
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            isbn10 = input("Enter the ISBN-10: ")
            isbn13 = input("Enter the ISBN-13: ")
            book_index = self.find_book_by_isbn(isbn10, isbn13)
        elif choice == '2':
            title = input("Enter the title: ")
            book_index = self.find_book_by_title(title)

        if book_index != -1:
            print("Book found:")
            print(self.books[book_index])
            print("Enter the new information (leave blank to retain old information):")
            for key, value in self.books[book_index].BookInfo.items():
                new_value = input(f"{key}: ")
                if new_value:
                    self.books[book_index].BookInfo[key] = new_value

            confirm = input("You have made changes. Do you want to save them? (yes/no): ")
            if confirm.lower() == "yes":
                print("Book information updated successfully.")
            else:
                print("Changes were not saved.")
        else:
            print("No matching books found.")

    def store_search_results(self, search_results, file_name):
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                for book in search_results:
                    for key, value in book.BookInfo.items():
                        file.write(f"{key}: {value}\n")
                    file.write("\n")

        except Exception as e:
            print("An error occurred while storing the results:", str(e))

    def archive_book(self):
        isbn10 = input("Enter the ISBN-10 of the book to archive: ")
        isbn13 = input("Enter the ISBN-13 of the book to archive: ")
        index = self.find_book_by_isbn(isbn10, isbn13)
        if index != -1:
            if self.books[index].num_copies > 1:
                n = int(input("Enter the number of copies to archive: "))
                if n > self.books[index].num_copies or n < 1:
                    print("Invalid number of copies.")
                else:
                    if n == self.books[index].num_copies:
                        confirm = input("Are you sure you want to archive this book? (yes/no): ")
                        if confirm.lower() == 'yes':
                            self.archive_books.append(self.books[index])
                            self.books.pop(index)
                            print("Book archived successfully.")
                        else:
                            print("Operation cancelled.")
                    else:
                        self.books[index].num_copies -= n
                        confirm = input("Are you sure you want to archive this book? (yes/no): ")
                        if confirm.lower() == 'yes':
                            self.archive_books.append(self.books[index])
                            self.archive_books[-1].num_copies = n
                            print("Book archived successfully.")
                        else:
                            print("Operation cancelled.")
            else:
                confirm = input("Are you sure you want to archive this book? (yes/no): ")
                if confirm.lower() == 'yes':
                    self.archive_books.append(self.books[index])
                    self.books.pop(index)
                    print("Book archived successfully.")
                else:
                    print("Operation cancelled.")
        else:
            print("Book not found.")

    def remove_book(self):
        print("Remove book:")
        isbn10 = input("Enter the ISBN-10 of the book to remove: ")
        isbn13 = input("Enter the ISBN-13 of the book to remove: ")
        for i in range(len(self.archive_books)):
            if self.archive_books[i].BookInfo["ISBN-10"] == isbn10 and self.archive_books[i].BookInfo[
                "ISBN-13"] == isbn13:
                confirm = input("Are you sure you want to remove this book? (yes/no): ")
                if confirm.lower() == 'yes':
                    self.archive_books.pop(i)
                    print("Book removed successfully.")
                    return
                else:
                    print("Operation cancelled.")
                    return
        print("Book not found.")

    def count_books_newer_than(self, year):
        newer_books=0
        for book in self.books:
            if "Year" in book.BookInfo:
                if int(book.BookInfo['Year']) > year :
                    newer_books+=1
        return newer_books

    def generate_reports(self):
        total_books = sum([book.num_copies for book in self.books])
        unique_books = len(self.books)
        archived_books = sum([book.num_copies for book in self.archive_books])
        publishers = {book.BookInfo['Publisher'] for book in self.books}

        book_dist_by_year = {}
        for book in self.books:
            if "Year" in book.BookInfo:
                Year=book.BookInfo['Year']

                if Year in book_dist_by_year:
                    book_dist_by_year[Year]+=1
                else:
                    book_dist_by_year[Year] = 1



        book_dist_by_publisher = {book.BookInfo['Publisher']: sum(
            [1 for b in self.books if b.BookInfo['Publisher'] == book.BookInfo['Publisher']]) for book in self.books}

        # prompt the user for a year
        year = int(input("Enter a year to find the number of books that are newer: "))
        books_newer_than_year = self.count_books_newer_than(year)

        print(f"Total books in LMS: {total_books}") #1
        print(f"Total unique books in LMS: {unique_books}")#2
        print(f"Total books archived: {archived_books}")#3
        print(f"Number of books newer than {year}: {books_newer_than_year}")#4

        print(f"Books distribution by the publisher: ")
        for Publisher,NBooks in book_dist_by_publisher.items():
            print(f"\t\tnumber of books from {Publisher}:{NBooks}")

        print(f"Books distribution by year: ")#5
        for Year ,NBooks in book_dist_by_year.items():
            print(f"\t\tnumber of books in {Year}:{NBooks}")


    def load_archieved_books(self):
        try:
            file_name = "lms_archive.txt"  # Name of the LMS file to store data
            with open(file_name, 'r', encoding='utf-8') as file:
                book_info = {}
                for line in file:
                    if line == "                                               \n":
                        self.archive_books.append(Book(book_info))
                        book_info = {}
                    else:
                        key, value = line.split(":")
                        book_info[key.strip()] = value.strip()
            print("Archived books loaded successfully.")
        except Exception as e:
            print("An error occurred while loading archived books:", str(e))


    def exit_system(self):
        try:
            file_name = "lms_data.txt"  # Name of the LMS file to store data
            with open(file_name, 'w', encoding='utf-8') as file:
                for book in self.books:
                    for key, value in book.BookInfo.items():
                        file.write(f"{key} : {value}\n")
                    file.write("                                               \n")

            print ("Library Management System terminated. Books data saved to file:", file_name)

            file_name = "lms_archive.txt"  # Name of the LMS file to store data
            with open(file_name, 'w', encoding='utf-8') as file:
                for book in self.archive_books:
                    for key, value in book.BookInfo.items():
                        file.write(f"{key} : {value}\n")
                    file.write("                                               \n")


            print("Library Management System terminated. Books data saved to file:", file_name)
        except Exception as e:
            print("An error occurred while saving data:", str(e))
        finally:
            # Terminate the program
            import sys
            sys.exit()
