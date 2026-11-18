# AGENTS.md

School ML project (420-5G4) split into three independent parts. All user-facing text, comments, and UI messages are in French; keep new ones French too.

## Layout

- `apprentissage/` — Pokemon dataset analysis + scikit-learn training/prediction notebooks.
- `analyse_image/` — Fashion-MNIST CNN training and image-classification inference notebooks.
- `agent/` — standalone C++17 library-management CLI (`bibliotheque`), not connected to the notebooks.
- `data/` — Pokemon CSVs. `modele/` — tracked Pokemon model. `analyse_image/modele/` — tracked Keras model.

## C++ (`agent/`)

Build from `agent/` (console executable `build/bibliotheque`, pybind11 module `build/bibliotheque_py*.so`):

```bash
mkdir -p build && cd build && cmake .. && make
```

Run with the bundled sample data; without `-d` the program starts empty and cannot save:

```bash
./build/bibliotheque -d data
```

- `CMakeLists.txt` builds a `core` static library from the explicit `CORE_SOURCES` list; add new core `.cpp` files there (there is no glob).
- Python bindings live in `bindings.cpp` and use `agent/.venv` (pybind11 + customtkinter). CMake auto-detects that venv. Import with `PYTHONPATH=build .venv/bin/python`; search/list bindings return copies, while `find_book_by_isbn`/`find_user_by_id` return mutable references tied to the `Library`.
- No test, lint, or formatter setup. Compilation must stay clean under `-Wall -Wextra -Wpedantic` (C++17).
- Persistence format is pipe-delimited `agent/data/books.txt` (`title|author|isbn|1/0|borrowerId`) and `agent/data/users.txt` (`name|userId|isbn1,isbn2`); keep `toString`/`toFileFormat`/`fromFileFormat` consistent.
- The root `.vscode/settings.json` points `cmake.sourceDirectory` at a Windows path; ignore it and use CLI CMake from `agent/`. `agent/.vscode/settings.json` only wires IntelliSense to `build/compile_commands.json`.
- GUI/X11 devcontainer config lives only in `agent/.devcontainer/`.

## Notebooks

Run each notebook with its own folder as the working directory; all data/model paths are relative:

- From `apprentissage/`: reads `../data/*.csv`, writes `../modele/modele_pokemon.mod`.
- From `analyse_image/`: reads `datas/fashion-mnist_train.csv` and `datas/fashion-mnist_test.csv`, reads/writes `modele/modele.json` and `modele/modele.weights.h5`, and reads `image/*.jpg`.

`analyse_image/datas/` is gitignored and absent from the repo: Fashion-MNIST CSVs must be supplied there before running `classification.ipynb`.

Notebook runs modify tracked artifacts: `apprentissage/partie_1-2.ipynb` overwrites `data/dataset.csv`, training overwrites `modele/modele_pokemon.mod`, and image training overwrites `analyse_image/modele/*`. Avoid re-running these unless the task intends to regenerate models/data.

There is no `requirements.txt`/`pyproject.toml`; Python dependencies are unpinned. Expected libraries: numpy, pandas, scikit-learn, joblib, matplotlib, seaborn, tensorflow/keras, Pillow.
