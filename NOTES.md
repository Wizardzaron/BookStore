# Project Shared Notes

## Daisy
Please update requirements.txt if you install more stuff.

```shell
# activate environent
pip freeze > requirements.txt
```

Sample DataSet Resources:
- [2023 Hardcover Nonfiction Best Sellers](https://www.nytimes.com/books/best-sellers/2023/04/23/hardcover-nonfiction/)
- [2021 Best Book Winners](https://www.nytimes.com/interactive/2021/12/28/books/best-book-winners.html)

> Note: I used ratings count on Amazon for `stock` values.

How to make a UUID
```shell
# open new terminal
python3
import uuid
uuid.uuid4()
```

**Use MongoDB Compass to Export Data**
1. `Export Full Collection`
2. With All Fields Selected, `Select Output`
3. Export File Type `JSON`

**Use MongoDB Compass to Import Data**
1. Create Database (Database Name: `bookstore`, Collection Name: `books`)
2. `Add Data`
3. Import JSON file
4. select `books.json` file found within this repo.
4. `Import`

## Ryan