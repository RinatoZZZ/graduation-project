from db import db_session
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User


app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

admin = Admin(app, name='Администратор бота "Face ID"', template_mode='bootstrap3')

class UserModelView(ModelView):
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
			link_photo='Ссылка на фото', 
			name='Имя', 
			username='Никнейм',
			)
	# vector_photo telegram_id	


admin.add_view(UserModelView(User, db_session, name="Пользователи"))




@app.route('/')
def index():
	title = "Face ID. Администратор"
	return "Администратор бота"


if __name__ == '__main__':
	app.run(debug=True)
