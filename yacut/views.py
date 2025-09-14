from flask import flash, render_template, redirect

from . import app, db
from .forms import UrlForm, FileForm
from .models import URLMap
from .ya_disk import upload_files_to_disk
from .utils import generate_short_id, check_short_id


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id_view():
    form = UrlForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            if not check_short_id(custom_id):
                flash('Недопустимый формат короткой ссылки')
                return render_template('index.html', form=form)
            if custom_id == 'files':
                flash(f'Имя {custom_id} нельзя использовать!')
                return render_template('index.html', form=form)
            if URLMap.query.filter_by(short=custom_id).first():
                flash(f'Имя {custom_id} уже занято!')
                return render_template('index.html', form=form)
        else:
            custom_id = generate_short_id()
        url = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, url=url)
    return render_template('index.html', form=form)


@app.route('/<string:short_url>', methods=['GET'])
def redirect_view(short_url):
    url = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(url.original)


@app.route('/upload-file', methods=['POST', 'GET'])
async def upload_file_view():
    form = FileForm()
    if form.validate_on_submit():
        urls = await upload_files_to_disk(form.files.data)
        for url in urls:
            short_url = generate_short_id(url)
            URLMap.create(url, short_url)
    return render_template('files.html', form=FileForm(), urls=urls)
