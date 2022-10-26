import os
from db import db_session
from flask import Flask, url_for, Markup
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User


app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

admin = Admin(app, name='Администратор бота "Face ID"', template_mode='bootstrap3')

class UserView(ModelView):
#	can_delete = False  # disable model deletion
	page_size = 50
	column_exclude_list = ['vector_photo', ]
	column_editable_list = ['check_photo', 'in_active']
	create_modal = True
	edit_modal = True
	column_labels = dict(check_photo='Подтвержденное фото', 
						date_time_registration='Дата и время регистрации', 
						in_active='Активность', 
						last_time_active='Последняя активность', 
						link_photo='Фото', 
						name='Имя', 
						username='Никнейм',
	)
	
	
	
	# ВЫВОД ФОТО В АДМИНКУ
	# ---------------------------------------------------------------------------------------------------
	
	def _list_thumbnail(view, context, model, name):
		if not model.link_photo:
			return ''
		url = url_for('static', filename=os.path.join('user_photo/', model.link_photo))
		if model.link_photo.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
			return Markup(f'<img src={url} width="70">')

    # передаю функцию _list_thumbnail в поле link_photo
	column_formatters = {
		'link_photo': _list_thumbnail
	}	

	# ---------------------------------------------------------------------------------------------------
	
	

admin.add_view(UserView(User, db_session, name="Пользователи"))


@app.route('/')
def index():
	title = "Face ID. Администратор"
	return "Администратор бота"


if __name__ == '__main__':
	app.run(debug=True)
