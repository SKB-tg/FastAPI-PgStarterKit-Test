from fastapi import FastAPI, Depends
from typing import Optional, Generator
from celery import Celery
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.parser_job.parser_f import MyUniParser
from dataclasses import dataclass
from app import crud, models, schemas
from app.settings import settings

app = FastAPI()

def get_db() -> Session:
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


@dataclass
class ParserData:
	kategory: str = "Менеджер по продажам"
	url: str = 'https://rabota.by/vacancies/menedzher_po_prodazham'
	page: int = 1
	fd: int = 1
	max_count_vacancy: int = 5
	chat_id: int = settings.CHAT_ID_PARS
	bot_token = settings.BOT_TOKEN 
 #***************   Случай с Celery *************
# создаем экземпляр Celery
# celery = Celery(
#     "tasks",
#     broker="redis://localhost:6367",
# )
# # настройка Celery
# celery.conf.task_routes = {"tasks.scrape_data": "scrape-queue"}

# @celery.task(name="tasks.scrape_data")
 # ************************************************
def parse_data_vacancy(data: Optional[ParserData], db: Session = get_db()):
	# работать можно с различными списками
	# url_list_p = [
	# url,
	# url+"?page=2&hhtmFrom=vacancy_search_list"
	# ]
	# pag = 1 # from setting import pag колич.сканируемых страниц
	# fd = 3 # дней назад
	item_in = schemas.vakancy.VakancyCreate()
	parser = MyUniParser(chat_id=data.chat_id, bot_token=data.bot_token)
	html = parser.get_requests_html(data.url)
	list_vacancy = parser.parse_data(html, data.kategory, data.page, data.fd,
	max_count=data.max_count_vacancy)
	for v in list_vacancy:
		v['ID вакансии'] = item_in.id_vakancy
		v['категории'] = item_in.kategory
		v['Наименование vakancy'] = item_in.name
		v['Компания'] = item_in.company
		v['Заработок'] = item_in.price 
		v['Краткое описание'] = item_in.description_short
		v['link vakancy'] = item_in.link
		v['Подробное описание'] = item_in.description_full
		v['Дата размещения'] = item_in.date_publikate
		res = crud.vakancy.create(db, obj_in=item_in)
	return {"message": "Данные успешно отправлены и сохранены в базе!"}
