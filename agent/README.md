# Construction du projet

Le projet utilise CMake (C++17). Depuis `agent/` :

```bash
mkdir -p build
cd build
cmake ..
make
```

L'exécutable console est produit dans `build/bibliotheque`.

# Répertoire data

Il contient 2 fichiers `books.txt` et `users.txt` que vous pouvez utiliser pour tester le code.
Il suffit de donner le chemin vers le répertoire data avec `bibliotheque -d <chemin vers data>` :

```bash
./build/bibliotheque -d data
```

# Bindings Python (pybind11)

Le module `bibliotheque_py` est construit en même temps que l'exécutable à partir de `bindings.cpp`.
Il expose les classes `Book`, `User`, `Library` et `FileManager`.

Un environnement Python local est utilisé pour l'interface graphique :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pybind11 customtkinter
```

CMake détecte automatiquement le `.venv` du projet. Pour construire :

```bash
mkdir -p build
cd build
cmake ..
cmake --build .
```

Le module est produit dans `build/bibliotheque_py.cpython-*.so`. Pour l'importer depuis `agent/` :

```bash
PYTHONPATH=build .venv/bin/python
```

```python
from bibliotheque_py import Book, User, Library, FileManager

bibliotheque = Library()
bibliotheque.add_book(Book("Le Petit Prince", "Antoine de Saint-Exupéry", "9782070612758"))
bibliotheque.add_user(User("Marie Dubois", "USR001"))

if bibliotheque.check_out_book("9782070612758", "USR001"):
    livre = bibliotheque.find_book_by_isbn("9782070612758")
    print(livre.to_string())

gestionnaire = FileManager("data/books.txt", "data/users.txt")
gestionnaire.load_library_data(bibliotheque)
gestionnaire.save_library_data(bibliotheque)
```

L'interface graphique peut ensuite être écrite avec `customtkinter` dans `agent/.venv`.
