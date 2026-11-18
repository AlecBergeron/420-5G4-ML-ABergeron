#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "book.h"
#include "filemanager.h"
#include "library.h"
#include "user.h"

namespace py = pybind11;

namespace {

std::vector<Book> copiesOf(const std::vector<Book*>& books) {
    std::vector<Book> copies;
    copies.reserve(books.size());
    for (const Book* book : books) {
        copies.push_back(*book);
    }
    return copies;
}

std::vector<User> copiesOf(const std::vector<User*>& users) {
    std::vector<User> copies;
    copies.reserve(users.size());
    for (const User* user : users) {
        copies.push_back(*user);
    }
    return copies;
}

}  // namespace

PYBIND11_MODULE(bibliotheque_py, m) {
    m.doc() = "Bindings pybind11 pour la bibliothèque C++";
    m.attr("__version__") = "0.1.0";

    py::class_<Book>(m, "Book")
        .def(py::init<>())
        .def(py::init<const std::string&, const std::string&, const std::string&>(),
             py::arg("title"), py::arg("author"), py::arg("isbn"))
        .def_property("title", &Book::getTitle, &Book::setTitle)
        .def_property("author", &Book::getAuthor, &Book::setAuthor)
        .def_property("isbn", &Book::getISBN, &Book::setISBN)
        .def_property("is_available", &Book::getAvailability, &Book::setAvailability)
        .def_property("borrower_id", &Book::getBorrowerId, &Book::setBorrowerId)
        .def("check_out", &Book::checkOut, py::arg("borrower_id"))
        .def("return_book", &Book::returnBook)
        .def("to_string", &Book::toString)
        .def("to_file_format", &Book::toFileFormat)
        .def("from_file_format", &Book::fromFileFormat, py::arg("line"))
        .def("__str__", &Book::toString);

    py::class_<User>(m, "User")
        .def(py::init<>())
        .def(py::init<const std::string&, const std::string&>(),
             py::arg("name"), py::arg("user_id"))
        .def_property("name", &User::getName, &User::setName)
        .def_property("user_id", &User::getUserId, &User::setUserId)
        .def_property_readonly("borrowed_books", &User::getBorrowedBooks)
        .def("borrow_book", &User::borrowBook, py::arg("isbn"))
        .def("return_book", &User::returnBook, py::arg("isbn"))
        .def("has_borrowed_book", &User::hasBorrowedBook, py::arg("isbn"))
        .def("borrowed_book_count", &User::getNumberOfBorrowedBooks)
        .def("to_string", &User::toString)
        .def("to_file_format", &User::toFileFormat)
        .def("from_file_format", &User::fromFileFormat, py::arg("line"))
        .def("__str__", &User::toString);

    py::class_<Library>(m, "Library")
        .def(py::init<>())
        .def("add_book", &Library::addBook, py::arg("book"))
        .def("remove_book", &Library::removeBook, py::arg("isbn"))
        .def("find_book_by_isbn", &Library::findBookByISBN, py::arg("isbn"),
             py::return_value_policy::reference_internal)
        .def("search_books_by_title",
             [](Library& library, const std::string& title) {
                 return copiesOf(library.searchBooksByTitle(title));
             },
             py::arg("title"))
        .def("search_books_by_author",
             [](Library& library, const std::string& author) {
                 return copiesOf(library.searchBooksByAuthor(author));
             },
             py::arg("author"))
        .def("get_available_books",
             [](Library& library) { return copiesOf(library.getAvailableBooks()); })
        .def("get_all_books",
             [](Library& library) { return copiesOf(library.getAllBooks()); })
        .def("add_user", &Library::addUser, py::arg("user"))
        .def("find_user_by_id", &Library::findUserById, py::arg("user_id"),
             py::return_value_policy::reference_internal)
        .def("get_all_users",
             [](Library& library) { return copiesOf(library.getAllUsers()); })
        .def("check_out_book", &Library::checkOutBook, py::arg("isbn"), py::arg("user_id"))
        .def("return_book", &Library::returnBook, py::arg("isbn"))
        .def("total_books", &Library::getTotalBooks)
        .def("available_book_count", &Library::getAvailableBookCount)
        .def("checked_out_book_count", &Library::getCheckedOutBookCount);

    py::class_<FileManager>(m, "FileManager")
        .def(py::init<const std::string&, const std::string&>(),
             py::arg("books_file"), py::arg("users_file"))
        .def("save_library_data", &FileManager::saveLibraryData, py::arg("library"))
        .def("load_library_data", &FileManager::loadLibraryData, py::arg("library"))
        .def("save_books_to_file", &FileManager::saveBooksToFile, py::arg("library"))
        .def("save_users_to_file", &FileManager::saveUsersToFile, py::arg("library"))
        .def("load_books_from_file", &FileManager::loadBooksFromFile, py::arg("library"))
        .def("load_users_from_file", &FileManager::loadUsersFromFile, py::arg("library"))
        .def("file_exists", &FileManager::fileExists, py::arg("filename"))
        .def("create_backup", &FileManager::createBackup);
}
