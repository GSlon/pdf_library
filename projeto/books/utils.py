import os
import secrets
from flask import url_for, current_app


def save_book_file(pdfile) -> str:
    ''' сохраняем на диск
        возвращаем не полный путь, а только начиная с директории book
    '''

    random_hex = secrets.token_hex(8)
    book_file_name = random_hex + str(pdfile.filename).strip().replace(' ', '')
    book_path = os.path.join(current_app.root_path, 'static/book', book_file_name)

    pdfile.save(book_path)

    return os.path.join('book', book_file_name)
