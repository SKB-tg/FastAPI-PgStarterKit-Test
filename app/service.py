from fastapi import FastAPI, Depends
from typing import Optional, Generator, List
from celery import Celery
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.parser_job.parser_f import MyUniParser
from dataclasses import dataclass
from app import crud, models, schemas
from app.settings import settings
import json

app = FastAPI()

def get_db() -> Session:
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


@dataclass
class ParserData:
	kategory: str 
	url: str #= 'https://rabota.by/vacancies/menedzher_po_prodazham'
	page: int# = 1
	fd: int# = 1
	max_count_vacancy: int# = 5
	chat_id: int# = settings.CHAT_ID_PARS
	bot_token: str# = settings.BOT_TOKEN

parser_data_def = ParserData(
	"Менеджер по продажам",
	'https://rabota.by/vacancies/menedzher_po_prodazham',
	1, 1, 5,
	settings.CHAT_ID_PARS,
	settings.BOT_TOKEN 
)
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
def parse_data_vacancy(db: Session, owner_id: int, data: ParserData = parser_data_def) -> List[schemas.vakancy.VakancyExt]:
	# работать можно с различными списками
	# url_list_p = [
	# url+"?page=2&hhtmFrom=vacancy_search_list"
	list_item_out = []
	item_in = schemas.VakancyCreate()
	parser = MyUniParser(chat_id=data.chat_id, bot_token=data.bot_token)
	html = parser.get_requests_html(data.url)
	list_vacancy = parser.parse_data(html, data.kategory, data.page, data.fd, db,
	max_count=data.max_count_vacancy)
	if list_vacancy is None:
		return  None
	for v in list_vacancy:
		item_in.id_vakancy = v['ID вакансии']
		item_in.name = v['Наименование vakancy']
		item_in.kategory = v['категории']
		item_in.link = v['link_vakancy']
		item_in.company = v['Компания']
		item_in.price = v['Заработок'] 
		item_in.description_full = v['Подробное описание']
		item_in.description_short = item_in.description_full[:70] + "..."
		item_in.date_publikate = v['Дата размещения']
		resu = crud.vakancy.get_id_vakancy(db, item_in.id_vakancy)
		print(76,item_in)
		message_id = v['message_id'] 

		#print(78, resu.__dict__)


		if resu:
			#resul = crud.vakancy.update(db, db_obj=resu, obj_in=item_in)
			# print(77, resu.__dict__)
			item_out = crud.vakancy.convert_schemas_to_model(item_in)
			resu.link = message_id
			list_item_out.append(resu)
		else:
			res = crud.vakancy.create_with_owner(db, obj_in=item_in, owner_id=owner_id)
			res.link = message_id
			print(87, res.__dict__)
	
			list_item_out.append(res)
	return list_item_out



