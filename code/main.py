from flask import Flask, render_template, redirect
from data import db_session
from data.clients import Client
import datetime
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/timetable.db")

    @app.route("/list")
    def index():
        db_sess = db_session.create_session()
        client = db_sess.query(Client).all()
        return render_template("index.html", client=client)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(Client).filter(Client.name == form.name.data).first():
                return render_template('register.html', title='Запись',
                                       form=form,
                                       message="Такой клиент уже есть")
            client = Client(
                name=form.name.data,
                number=form.number.data,
                about=form.about.data,
                date=form.date.data
            )
            db_sess.add(client)
            db_sess.commit()
            return redirect('/list')
        return render_template('register.html', title='Запись', form=form)

    app.run()


if __name__ == '__main__':
    main()
