from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
import bcrypt
from bson import ObjectId


#adding/creating mongo
mongo_client = pymongo.MongoClient("mongodb://admin:admin@mongodb:27017", connect=True)
db = mongo_client['profiles']
profiles_collections = db['profiles']

app = Flask(__name__, template_folder='templates')
app.secret_key = 'secret_key'


comments = []

@app.route("/", methods=['GET', 'POST'])
@app.route("/main", methods=['GET', 'POST'])
@app.route("/nightthoughts", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # Обработка данных, отправленных из формы
        comment_content = request.form['comment']
        comments.append(comment_content)  # Добавление комментария в хранилище

        # После обработки комментария можно перенаправить пользователя или выполнить другие действия

    # Возвращает страницу с формой и текущим списком комментариев
    return render_template('main.html', comments=comments)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        # Обработка данных формы
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        #incryption of the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        profiles_data = {
            "username": username,
            "email": email,
            "password": hashed_password.decode('utf-8')
        }
        
        result_profiles = profiles_collections.insert_one(profiles_data)
        
        #временная сессия
        #session['username'] = username
        #session['email'] = email

        # Перенаправление на страницу профиля после успешной регистрации
        #return redirect(url_for('profile/<user_id>'), user_id=str(result_profiles.inserted_id)) # user_id=1
        return redirect(url_for('about'))
    return render_template("reg.html")

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    profiles_data = profiles_collections.find_one({"_id": ObjectId(user_id)})
    
    # Проверка наличия пользователя в базе данных
    if profiles_data:
        return render_template('profile.html', user=profiles_data)
    else:
        return "Not found."
    
    #return render_template('profile.html', user=user, comments=comments)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)