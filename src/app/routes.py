from config import Config
from database import ShortUrls
from flask import Markup, flash, redirect, render_template, request, url_for
from models import NewUrl

from app import app


db = ShortUrls()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NewUrl(request.form)
    copy_link = ""
    if request.method == 'POST':
        long_url = request.form['long_url']
        if form.validate():
            short_url = db.add_url(long_url)
            uid = short_url if short_url else db.find_short_url(long_url)
            dom = Config.DOMAIN_NAME if Config.DOMAIN_NAME else request.host
            copy_link = 'http://' + dom + ':5000/' + uid
        else:
            flash("Not a valid URL")

    return render_template(
        'index.html',
        form=form,
        css=['main.css'],
        copy_link=copy_link
    )

@app.route('/<short_id>')
def redirect_url(short_id):
    link = db.get_original_url(short_id)
    if link:
        return redirect(link)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))
