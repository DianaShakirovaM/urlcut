from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidApiUsage
from .utils import generate_short_id, check_short_id
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidApiUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidApiUsage('\"url\" является обязательным полем!')
    if 'short_link' in data:
        short_link = data['short_link']
        if not check_short_id(short_link) or len(short_link) > 16:
            raise InvalidApiUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        elif short_link == 'files':
            raise InvalidApiUsage(f'Имя {short_link} нельзя использовать!')
        elif URLMap.query.filter_by(short=short_link).first():
            raise InvalidApiUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        short_link = generate_short_id()
    url = URLMap(
        original=data['url'],
        short=short_link
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short_id=short_id).first()
    if url is None:
        raise InvalidApiUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
