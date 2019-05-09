from QueryHandler import QueryHandler

#query_handler = QueryHandler('10.42.0.251', 9050)
query_handler = QueryHandler('192.168.129.196', 9050)
#query_handler = QueryHandler('localhost', 9999)

def get_genres():
    response = query_handler.send_request("GETGENRES", None)
    return response

def get_regions():
    response = query_handler.send_request("GETTOWNS", None)
    return response

def get_all_books(login = ''):
    response = query_handler.send_request("GETBOOKALL", {'Login': login})
    return response

def get_books_by_genre(genre_id, login = ''):
    response = query_handler.send_request("GETBOOK", {"GenreId": genre_id, "Login": login})
    return response

def get_users_book(user_id):
    response = query_handler.send_request("GETUSERBOOKS", {"Login": user_id})
    return response

def add_book_to_library(book_id, login):
    query_handler.send_request("SETUSERBOOK", {"BookId": book_id, "Login": login})

def delete_book_from_library(book_id, login):
    query_handler.send_request("DELUSERBOOK", {"BookId": book_id, "Login": login})

def get_recommend_books(user_id, camrades):
    response = query_handler.send_request("GETBOOKREC", {"Login": user_id, "UsersLogins": camrades})
    return response

def get_full_book_info(book_id, login = None):
    response = query_handler.send_request("GETFULLBOOK", {"BookId": book_id, "Login": login})
    return response

def register_user(register_data):
    query_handler.send_request("SETUSER", register_data)

def login(login, password):
    login_data = {
    "Login": login,
    "Password": password
    }
    response = query_handler.send_request("LOGIN", login_data)
    return response

def save_log(login, genre_id):
    query_handler.send_request("SETLOG", {"Login": login, "GenreId": genre_id})

def get_data_for_clustering():
    response = query_handler.send_request("GETLOG", None)
    return response

def save_form_answers(form_result):
    query_handler.send_request("SETUSERPREF", form_result)

def get_short_event(user_id, camrades):
    response = query_handler.send_request("GETEVENTREC", {"Login": user_id, "UsersLogins": camrades})
    return response

def get_full_event_info(event_id):
    response = query_handler.send_request("GETFULLEVENT", {"EventId": event_id})
    return response

def save_mark(mark, login, book_id):
    response = quesry_handler.send_request("SAVEMARK", {"Rate": mark, "Login": login, "BookId": book_id})

def get_comments(book_id):
    response = query_handler.send_request("GETCOMMENTS", {"BookId": book_id})
    return response

def save_comment(comment):
    query_handler.send_request("SAVECOMMENT", comment)
