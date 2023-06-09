# BookStore API
Final Project for CPSC 449, SPRING 2023

Team Members (Group 17):
- Daisy Catalan
- Ryan Haddadi

Tech Stack
- Python 3.9+ (Specifically using Python 3.10.6)
- FastAPI
- MongoDB
- Pydantic

# Get Started

Clone the Project
```shell
git clone https://github.com/Wizardzaron/BookStore.git
cd BookStore/
```

Create an environment
```shell
# Linux
python3 -m venv .venv

# Windows
py -3 -m venv .venv

```

Activate the environment
```shell
# Linux
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

Open bookstore API docs: http://127.0.0.1:8000/docs


[Notes](/NOTES.md)
