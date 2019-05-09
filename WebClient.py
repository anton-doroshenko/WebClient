from flask import Flask, render_template, abort, request, redirect, url_for, session, g, url_for
import json
import urllib.request
import requests
import socket
from QueryHandler import QueryHandler
import Repository
import Clustering

app = Flask(__name__)
app.secret_key = "some_secrete"

CLUSTERS = {}

PRODUCTS = {
    'iphone': {
        'name': 'iPhone 5S',
        'category': 'Phones',
        'price': 699,
    },
    'galaxy': {
        'name': 'Samsung Galaxy 5',
        'category': 'Phones',
        'price': 649,
    },
    'ipad-air': {
        'name': 'iPad Air',
        'category': 'Tablets',
        'price': 649,
    },
    'ipad-mini': {
        'name': 'iPad Mini',
        'category': 'Tablets',
        'price': 549
    }
}

BOOKS = [{'BookId': 1, 'Name': 'Тонкое Искуство', 'NotInLib': 1, 'ImageUrl': '../static/images/book.svg'},
{'BookId': 2, 'Name': 'Исповедь Чудовеща', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 3, 'Name': 'Хочу і буду', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 4, 'Name': 'Сила нтроверта', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 2, 'Name': 'Исповедь Чудовеща', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 3, 'Name': 'Хочу і буду', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 4, 'Name': 'Сила нтроверта', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 2, 'Name': 'Исповедь Чудовеща', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 3, 'Name': 'Хочу і буду', 'NotInLib': 1, 'ImageUrl': 'sss'},
{'BookId': 4, 'Name': 'Сила нтроверта', 'NotInLib': 1, 'ImageUrl': 'sss'}]

@app.route("/", methods=['GET','POST'])
@app.route("/home")
def home():
    is_get_by_genre = False
    new_books = []
    event = {}
    #todo кєшировать
    genres = Repository.get_genres()
    regions = Repository.get_regions()
    print(regions)
    #regions = [{'RegionId': 1, 'Name': 'dsds'}, {'RegionId': 1, 'Name': 'dsds'}]
    print(genres)
    print(g.user)
    if request.method == 'GET':
        if g.user:
            logs = Repository.get_data_for_clustering()
            print(logs)
            #input()
            CLUSTERS = {}
            print(CLUSTERS)
            CLUSTERS = Clustering.get_clusters(logs)
            print(CLUSTERS)
            camrades = []
            for cluster in CLUSTERS.values():
                print(session['user'])
                print(cluster)
                if session['user'] in cluster:
                    camrades = cluster
            print(camrades)
            data = Repository.get_recommend_books(session['user'], camrades)
            new_books = Repository.get_all_books(session['user'])
            event = Repository.get_short_event(session['user'], camrades)
            print(data)
        else:
            data = Repository.get_all_books()
            event = {'LongPictureEvent' : '../static/images/eventMain.jpeg', 'EventId' : 1}

    #with open("./static/data_file.json", "r") as read_file:
    #    data = json.load(read_file)
    #print(data)
    if request.method == 'POST':
        button_value = request.form["button"]
        print("test" + request.form["button"])
        if button_value == "login":
            session.pop('user', None)
            result = Repository.login(request.form["username"], request.form["password"])
            if(result["Result"]):
                session['user'] = request.form["username"]
                g.user = session['user']
                print("EEeeeee")
                #data = Repository.get_all_books(session['user'])
                #################################
                logs = Repository.get_data_for_clustering()
                print(logs)
                #input()
                CLUSTERS = {}
                print(CLUSTERS)
                CLUSTERS = Clustering.get_clusters(logs)
                print(CLUSTERS)
                camrades = []
                for cluster in CLUSTERS.values():
                    print(session['user'])
                    print(cluster)
                    if session['user'] in cluster:
                        camrades = cluster
                print(camrades)
                data = Repository.get_recommend_books(session['user'], camrades)
                new_books = Repository.get_all_books(session['user'])
                event = Repository.get_short_event(session['user'], camrades)
                print(data)
                #######################################
            else:
                data = BOOKS
                event = {'LongPictureEvent' : '../static/images/eventMain.jpeg', 'EventId' : 1}
        elif button_value == "registration":
            print("_register_")
            print(request.form["name"])
            register_data = {
                "FirstName": request.form["name"],
                "LastName": request.form["surname"],
                "Login": request.form["login_box"],
                "Password": request.form["password"],
                "Email": request.form["email"],
                #"Age": request.form["age"],
                "Region": request.form["region"],
                "Sex": request.form["sex"],
                "LanguageId": 0,#request.form["lang"],
                "Birthday": str(request.form["age"]).replace('-', ''),#"10/10/2018",
                #"IsAdmin": '0',
                #"CardId": 1,
                "Residence": 0,
                "Religion": 0,
                "LevelLive": 0
            }
            print(register_data)
            #session['login'] = request.form["login_box"]

            result = Repository.register_user(register_data)
            return redirect(url_for("question_form", login = request.form["login_box"]))

            data = Repository.get_all_books()
        elif button_value == "logout":
            session.pop('user', None)
            data = Repository.get_all_books()
            g.user = None
        elif button_value == "addbook":
            print(request.form["book_id"])
            Repository.add_book_to_library(request.form["book_id"], session['user'])

            if g.user:
                logs = Repository.get_data_for_clustering()
                print(logs)
                #input()
                CLUSTERS = {}
                print(CLUSTERS)
                CLUSTERS = Clustering.get_clusters(logs)
                print(CLUSTERS)
                camrades = []
                for cluster in CLUSTERS.values():
                    print(session['user'])
                    print(cluster)
                    if session['user'] in cluster:
                        camrades = cluster
                print(camrades)
                data = Repository.get_recommend_books(session['user'], camrades)
                new_books = Repository.get_all_books(session['user'])
                event = Repository.get_short_event(session['user'], camrades)
            #data = Repository.get_all_books(session['user'])
        elif button_value == "deletebook":
            print(request.form["book_id"])
            Repository.delete_book_from_library(request.form["book_id"], session['user'])

            if g.user:
                logs = Repository.get_data_for_clustering()
                print(logs)
                #input()
                CLUSTERS = {}
                print(CLUSTERS)
                CLUSTERS = Clustering.get_clusters(logs)
                print(CLUSTERS)
                camrades = []
                for cluster in CLUSTERS.values():
                    print(session['user'])
                    print(cluster)
                    if session['user'] in cluster:
                        camrades = cluster
                print(camrades)
                data = Repository.get_recommend_books(session['user'], camrades)
                new_books = Repository.get_all_books(session['user'])
                event = Repository.get_short_event(session['user'], camrades)
            #data = Repository.get_all_books(session['user'])
        else:
            is_get_by_genre = True
            if g.user:
                print("Iluha" + session['user'])
                Repository.save_log(session['user'], request.form["button"])
                data = Repository.get_books_by_genre(request.form["button"], session['user'])
            else:
                data = Repository.get_books_by_genre(request.form["button"])
    #data = BOOKS
    #print(data)
    #'http://bookmonsters.info/blog/wp-content/uploads/2016/10/IMG_3650-1280x200.jpg'}#'../static/images/event.jpg'}
    #return render_template('home.html', products=BOOKS, is_login=True, event=event)
    return render_template('home.html', products = data, genres = genres, is_login = g.user, new_books = new_books, event=event, regions=regions, is_get_by_genre = is_get_by_genre)#'''products=PRODUCTS''')

@app.route("/library")
def library():
    user = "guest"
    if g.user:
        user = session['user']
        print(user)
        books = Repository.get_users_book(user)
        print(books)
    return render_template('user_library.html', user= user, books = books, is_login = g.user)

@app.route("/book", methods=['GET','POST'])
def book():
    book = {
        "BookId": 1,
        "Name": 'cccacascac',
        "Descr": '''
            У творчому спадку Фридриха Ніцше «Ранкова зоря» – друга з трьох праць, що вирізняють середній («позитивістський») період філософування німецького мислителя. Посідаючи позицію між «Людським, надто людським» і «Веселою наукою», вона знаменує початок майбутнього проекту «переоцінки всіх цінностей». Текст складається з п’яти частин, які містять 575 афоризмів різної довжини й тематики. Ніцше визначає мораль як звичаєвий спосіб учинку й оцінювання. Порушено питання про передсуди, вільнодумство, проблеми істини та знання. Проведено підготовчу роботу з подальшого вивчення моралі та релігії, що розвиватиметься в полемічному трактаті «До генеалогії моралі» та критичній розвідці «Антихрист». В «Ранковій зорі» філософія Ніцше розглядається як експериментальна візія існування й випробування різноманітних перспектив самореалізації людини. Видання супроводжується історико-філософською передмовою й дослідницько-термінологічним коментарем. Українською твір перекладено вперше.
        '''
    }
    comments = [
    {'text': 'Я в захваті.',
    'author': 'Кочубей',
    'avatar': '../static/images/koch.jpeg'},
    {'text': 'Книга дуже цікава!',
    'author': 'Гість',
    'avatar': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIgycbgAB8-MjaOmORWGZgvHlh-nb0yUteILyub1nu8LJsNQ1_Sw'}
    ]

    regions = [{'RegionId': 1, 'Name': 'dsds'}, {'RegionId': 1, 'Name': 'dsds'}]
    book_id = request.args['book_id']
    login = ''
    if g.user:
        login = session['user']
        book = Repository.get_full_book_info(book_id, session['user'])
    else:
        book = Repository.get_full_book_info(book_id)

    comments = Repository.get_comments(book_id)

    if request.method == 'POST':
        print('sdfsdf')
        button_value = request.form["button"]
        print("test" + request.form["button"])
        if button_value == "registration":
            print("_register_")
            print(request.form["name"])
            print(request.form.get("sex"))
            print(type(request.form["date"]))
            register_data = {
                "FirstName": request.form["name"],
                "LastName": request.form["surname"],
                "Login": request.form["login_box"],
                "Password": request.form["password"],
                "Email": request.form["email"],
                #"Age": request.form["age"],
                "Region": request.form["region"],
                "Sex": request.form["sex"],
                "LanguageId": 0,#request.form["lang"],
                "Birthday": str(request.form["age"]).replace('-', ''),#"10/10/2018",
                #"IsAdmin": '0',
                #"CardId": 1,
                "Residence": 0,
                "Religion": 0,
                "LevelLive": 0
            }
            print(register_data)
        elif button_value == "send":
            comment = {'BookId': book_id, 'Login': login, 'Comment': request.form['comment_text']}
            Repository.save_comment(comment)
            return redirect(url_for("book", book_id = str(book_id)))
    return render_template('book_page.html', book = book, comments = comments, regions = regions, is_login = g.user)

@app.route("/questionnaire", methods=['GET','POST'])
def question_form():
    login = request.args['login']
    if request.method == 'POST':
        print(request.form["q2"])
        form_result = {
            "Login": login,
            "LanguageId": request.form["q2"],
            "AmountTimeId": request.form["q1"],
            "GenreId": request.form["q4"],
            "AuthorGenreId": 0
        }
        print(form_result)
        Repository.save_form_answers(form_result)
        Repository.save_log(login, request.form["q4"])
        return redirect(url_for('home'))
    return render_template('questionnaire.html')

@app.route("/event")
def event():
    event_id = request.args['EventId']
    full_event = Repository.get_full_event_info(event_id)
    print(full_event)
    return render_template('event.html', event = full_event)


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route("/#")
def menu_click():
    print("menu_clicked")
    print()
    return redirect(url_for('home'))

if __name__ == "__main__":


    #response = requests.get('http://0.0.0.0:9999?param=value')
    #print(response.read())
    #with open("./static/data_file.json", "r") as read_file:
    #    data = json.load(read_file)
    #print(data)
    #with open("./static/data_file.json", "w") as write_file:
        #json.dump(PRODUCTS, write_file)
    app.run(host='0.0.0.0', port=5000)
    #app.run(host='77.47.208.43', port=5000)
