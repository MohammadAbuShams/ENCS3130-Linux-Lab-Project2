class Book:
    def __init__(self, BookInfo):
        self.num_copies = 1
        self.BookInfo = BookInfo

    def __str__(self):
        for key, value in self.BookInfo.items():
            print(f"{key}: {value}")
        print(f"Number of Copies: {self.num_copies}")
        return "*******************************************"