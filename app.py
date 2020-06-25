from flask import Flask, render_template, g, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                        login_required, current_user)
import datetime
import forms
import models


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'Hohisdsan90(as8jfdshjk(=_+f0;;s}|]fdsDFEFge435245%J(F)'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database befire each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You've successfully registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
def index():
    """Home page to view all entries logged in or out"""
    # add functionality to go to next page if there are more than x entries
    entries = models.Entry.select().order_by(models.Entry.date_created.desc())
    return render_template('index.html', entries=entries)

@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def new_entry():
    """Make a new entry"""
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(title=form.title.data.strip(),
                            date_created=form.date_created.data,
                            content=form.content.data.strip(),
                            resources=form.resources.data,
                            time_spent=form.time_spent.data,
                            user=g.user._get_current_object())
        flash("New entry posted!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)

@app.route('/entries/<int:id>')
@login_required
def detail(id):
    """View an entry by id"""
    entries = models.Entry.select().where(models.Entry.id == id)
    # users = models.User.select().where(models.Entry.user_id == models.User.id)
    if entries.count == 0:
        abort(404)
    return render_template('detail.html', entries=entries)

@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    """Logged in user edit own existing entry"""
    form = forms.EntryForm()
    entry_user_id = models.Entry.select().where(models.Entry.id == id)
    if form.validate_on_submit():
        data = (models.Entry.update({models.Entry.title: form.title.data,
                                    models.Entry.date_created: form.date_created.data,
                                    models.Entry.content: form.content.data,
                                    models.Entry.resources: form.resources.data,
                                    models.Entry.time_spent: form.time_spent.data})
                            .where(models.Entry.id == id))
        data.execute()
        flash("Your changes have been saved!", "success")
        return redirect(url_for('index'))
    else:
        for entry in entry_user_id:
            if g.user.id == entry.user_id:
                data = models.Entry.select().where(models.Entry.id == id).get()
                form.title.data = data.title
                form.date_created.data = data.date_created
                form.content.data = data.content
                form.resources.data = data.resources
                form.time_spent.data = data.time_spent
            else:
                flash("You can't edit someone elses entry.")
                return redirect(url_for('index'))
    return render_template('edit.html', form=form)


@app.route('/entries/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    """Logged in user delete own existing entry"""
    entry_user_id = models.Entry.select().where(models.Entry.id == id)
    for entry in entry_user_id:
        if g.user.id == entry.user_id:
            models.Entry.delete().where(models.Entry.id == id).execute()
            flash("Your entry has been deleted!", "success")
            return redirect(url_for('index'))
        else:
            flash("You can't delete someone elses entry.")
            return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    models.initialize()
    entries = models.Entry.select()
    if len(entries) <= 0:
        try:
            models.Entry.get_or_create(
                title='Todays first entry',
                date_created=datetime.datetime.now(),
                content='This is todays first entry and there will be no duplicates.',
                resources='resources',
                time_spent=5,
                user=1
            )
            # models.User.create_user(
            #     username='testuser',
            #     email='test@example.com',
            #     password='password'
            # )
        except ValueError:
            pass
    else:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
