## API для "Системы управления университетом"
Это система, где учитываются студенты, преподаватели, курсы, группы, отделения университета, оценки и другие соответствующие данные.

### Установка
Клонируйте репозиторий https://github.com/NadinKon/test_FastAPI <br>
Установите зависимости с помощью pip: <br>
pip install -r requirements.txt

Сделайте необходимые настройки: имя своей базы данных и пароль. <br>
DATABASE_URI = 'postgresql://postgres:<your_password>@localhost/<name_of_the_datbase>'

В файле Untitled находится ER-диаграмма, которая описывает все сущности и связи между ними.

С помощью SQL скрипта из файла SQLskript можно создать все необходимые таблицы с полями, их типами данных, ключами и связями. 

В файле SQLqueries находятся следующие SQL запросы: <br>
- Выбрать всех студентов, обучающихся на курсе "Математика". <br>
- Обновить оценку студента по курсу. <br>
- Выбрать всех преподавателей, которые преподают в здании №3. <br>
- Удалить задание для самостоятельной работы, которое было создано более года назад. <br>
- Добавить новый семестр в учебный год.


### Использование
Запустите сервер разработки FastAPI:
uvicorn main:app --reload

Тестировать API можно по адресу: http://127.0.0.1:8000/docs#/

### Эндпоинты API 
- POST /students - создать нового студента.
- GET /students/{student_id} - получить информацию о студенте по его id.
- PUT /students/{student_id} - обновить информацию о студенте по его id.
- DELETE /students/{student_id} - удалить студента по его id.
- GET /teachers - получить список всех преподавателей.
- POST /courses - создать новый курс.
- GET /courses/{course_id} - получить информацию о курсе по его id.
- GET /courses/{course_id}/students - получить список всех студентов на курсе.
- POST /grades - создать новую оценку для студента по курсу.
- PUT /grades/{grade_id} - обновить оценку студента по курсу.

Этот проект использует FastAPI и SQLAlchemy для управления и сохранения данных. FastAPI используется для создания веб-API, а SQLAlchemy используется для взаимодействия с базой данных.
