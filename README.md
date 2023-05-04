# BookStore API
Final Project for CPSC 449, SPRING 2023

Team Members (Group 17):
- Daisy Catalan
- Ryan Haddadi

Tech Stack
- Python 3.7 or greater
- FastAPI
- MongoDB
- Pydantic

# Get Started

Create an environment
```shell
# macOS/Linux
python3 -m venv .venv

# Windows
py -3 -m venv .venv

```

Activate the environment
```shell
# macOS/Linux
. .venv/bin/activate

# Windows
.venv\Scripts\activate

```

Install the required packages in activated environment
```shell
# activate environment
pip install -r requirements.txt
```

Start the server
```shell
# activate the environment
uvicorn bookstore:app --reload
```

Open bookstore API docs
```shell
http://127.0.0.1:8000/docs
```

[Notes](/NOTES.md)