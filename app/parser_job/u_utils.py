#from fastapi import APIRouter, Request, Response
#from starlette.types import Message, Receive, Scope, Send
import os.path
from pathlib import Path
import typing
from typing import Callable, Dict, Any, Awaitable, Union, List, Optional, BinaryIO, cast
import json
from urllib.parse import parse_qs, parse_qsl
#from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy
#from aiohttp import hdrs


# async def empty_receive() -> typing.NoReturn:
#     raise RuntimeError("Receive channel has not been made available")


# async def empty_send(message: Message) -> typing.NoReturn:
#     raise RuntimeError("Send channel has not been made available")
def str_for_dict(str) -> dict:
    ad=str.replace('{', "").replace('}', "").split(',')
    ad1={i.split(":")[0].replace("'", ''):i.split(":")[1].replace("'", '')[1:] for i in ad}
    return ad1
#***************************************************
#----------------field_serializerВы также можете использовать :

import re
from pydantic import BaseModel, field_serializer

class MyModel(BaseModel):
    p: dict

    @field_serializer('p')
    def serialize_dict(values):
        for key, value in values.items():
            if isinstance(value, re.Pattern):
                values[key] = value.pattern
        return values

a = MyModel(p={"pattern": re.compile("asd")})

print(a.model_dump_json())
#***************************************************
from datetime import datetime, timedelta

def get_date_flag(date_str):
    today = datetime.now().date()
    yesterday = (today - timedelta(days=1))
    day_before_yesterday = (today - timedelta(days=2))

    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    if date == today:
        return 1 #'сегодня'
    elif date == yesterday:
        return 2 #'вчера'
    elif date == day_before_yesterday:
        return 3 #'позавчера'
    else:
        return 4 #'другой день'

#*************************************************************************
class TgUserCreate(object):
    """docstring for TgUserCreate"""
    def __init__(self, arg):
        super(TgUserCreate, self).__init__()
        self.arg = arg



def parse_webapp_init_data1( init_data: str, *, loads: Callable[..., Any] = json.loads,) -> TgUserCreate:

    result = {}
    for item in init_data.split():
        key, value = item.split('=')
        result[key.strip()] = value.strip().replace("'", "")
    result_out = {'id_chat': int(result.pop('id'))}
    for key, value in result.items(): 
        if value.lower() == 'none': result_out[key] = None 
        elif value.lower() == 'false': result_out[key] = False 
        elif value.lower() == 'true': result_out[key] = True 
        elif value.isdigit(): result_out[key] = int(value) 
        else:
            result_out[key] = value 
    return TgUserCreate(**result_out)

 # ``` Ключевые улучшения: - Мы используем метод `.split()` для преобразования строки в список, а не `.rsplit()`
 #  - Мы используем цикл `for item in init_data.split()` вместо цикла "for x in range(len(data))". Это более питонячий способ. 
 #  - Мы убрали условие `if key == 'id'` и использовали его значение для `id_chat` 
 #  - Мы использовали метод `.lower()` для сравнения строк вместо повторения кода 
 #  - Мы использовали метод `.isdigit()` для проверки, является ли значение числом 
 #  - Мы убрали лишнюю проверку `value.find("'")`, потому что она всегда будет истинной, если значение содержит какой-то текст.
 #   Вместо этого мы просто проверяем, является ли значение числом (`isdigit()`)

# def parse_webapp_init_data1(
#     init_data: str,
#     *,
#     loads: Callable[..., Any] = json.loads,) -> TgUserCreate:
    
#     data=init_data.rsplit(" ")
#     result={ data[x].split('=')[0].strip() : data[x].split('=')[1].strip()  for x in range(len(data))}
#     result_out={}
#     for key, value in result.items():
#         if key == 'id':
#             result_out['id_chat']=int(value)
#         else:
#             if value == 'None' or value == 'False' or value == 'True' :
#                 if value == 'None' or value == 'none' :
#                     result_out[key]=None
#                 if value == 'False':
#                     result_out[key]=bool(False)
#                 if value == 'True':
#                     result_out[key]=bool(True)
#             elif value.find("'"):
#                 result_out[key]=int(value)
#             else:
#                 result_out[key]=value.replace("'", "")
#     print(99, result_out)

#     return TgUserCreate(**result_out)

#************************************************************************************
def save_in_file(project_name: str, html_content: str):
    # Set the project directory
    project_dir = Path.cwd() / project_name
    os.makedirs(project_dir, exist_ok=True)
    #print(html_content)
    # Write the HTML content to the index.html file
    with open(project_dir / "index1.html", "w", encoding="utf-8") as f:
        #for l in html_content:
       f.write(html_content)

    # Write the JSON configuration file
    config = {
        "name": project_name,
        "version": 2,
    }

    with open(project_dir / "config.json", "w") as f:
        json.dump(config, f)

def read_file_str():

    dir_path=os.path.dirname( os.path.abspath(__file__))+"\\"+'input'
    try:
        list_f=os.listdir(dir_path)
        print(list_f)
        for l in list_f:
            with open( dir_path+"\\"+l, 'r', encoding='utf-8') as fi:
                with open("out\\"+l, "w", encoding='utf-8') as fw:
                    for line in fi:
                        fw.write(line)
    except Exception as e:
        print(e)
        return None
    return True



#********************************************
# class Methods(Request):
#     """docstring for Methods"""
#     def __init__(
#         self, *args, **kwargs): # scope: Scope, receive: Receive = empty_receive, send: Send = empty_send):
#         super().__init__(*args, **kwargs)
#         self.scope["type"] = "http"
#         self._receive = empty_receive
#         self._send = empty_send
#         self._stream_consumed = False
#         self._is_disconnected = False
#         #self.scope=scope
#     POST_METHODS = {
#     hdrs.METH_PATCH,
#     hdrs.METH_POST,
#     hdrs.METH_PUT,
#     hdrs.METH_TRACE,
#     hdrs.METH_DELETE,
#     }
#     async def post(self) -> MultiDictProxy[Union[str, bytes, FileField]]:
#         """Return POST parameters."""
#         self._post: Optional[MultiDictProxy[Union[str, bytes, FileField]]] = None
#         #self._method = message.method
#         if self._post is not None:
#             self._post = MultiDictProxy(MultiDict())
#             return self._post


        # if self._method not in self.POST_METHODS:
        #     self._post = MultiDictProxy(MultiDict())
        #     return self._post

        # content_type = self.content_type
        # if content_type not in (
        #     "",
        #     "application/x-www-form-urlencoded",
        #     "multipart/form-data",
        # ):
        #     self._post = MultiDictProxy(MultiDict())
        #     return self._post

        # out: MultiDict[Union[str, bytes, FileField]] = MultiDict()

        # if content_type == "multipart/form-data":
        #     multipart = await self.multipart()
        #     max_size = self._client_max_size

        #     field = await multipart.next()
        #     while field is not None:
        #         size = 0
        #         field_ct = field.headers.get(hdrs.CONTENT_TYPE)

        #         if isinstance(field, BodyPartReader):
        #             assert field.name is not None

        #             # Note that according to RFC 7578, the Content-Type header
        #             # is optional, even for files, so we can't assume it's
        #             # present.
        #             # https://tools.ietf.org/html/rfc7578#section-4.4
        #             if field.filename:
        #                 # store file in temp file
        #                 tmp = tempfile.TemporaryFile()
        #                 chunk = await field.read_chunk(size=2**16)
        #                 while chunk:
        #                     chunk = field.decode(chunk)
        #                     tmp.write(chunk)
        #                     size += len(chunk)
        #                     if 0 < max_size < size:
        #                         tmp.close()
        #                         raise HTTPRequestEntityTooLarge(
        #                             max_size=max_size, actual_size=size
        #                         )
        #                     chunk = await field.read_chunk(size=2**16)
        #                 tmp.seek(0)

        #                 if field_ct is None:
        #                     field_ct = "application/octet-stream"

        #                 ff = FileField(
        #                     field.name,
        #                     field.filename,
        #                     cast(io.BufferedReader, tmp),
        #                     field_ct,
        #                     field.headers,
        #                 )
        #                 out.add(field.name, ff)
        #             else:
        #                 # deal with ordinary data
        #                 value = await field.read(decode=True)
        #                 if field_ct is None or field_ct.startswith("text/"):
        #                     charset = field.get_charset(default="utf-8")
        #                     out.add(field.name, value.decode(charset))
        #                 else:
        #                     out.add(field.name, value)
        #                 size += len(value)
        #                 if 0 < max_size < size:
        #                     raise HTTPRequestEntityTooLarge(
        #                         max_size=max_size, actual_size=size
        #                     )
        #         else:
        #             raise ValueError(
        #                 "To decode nested multipart you need " "to use custom reader",
        #             )

        #         field = await multipart.next()
        # else:
        #     data = await self.read()
        #     if data:
        #         charset = self.charset or "utf-8"
        #         out.extend(
        #             parse_qsl(
        #                 data.rstrip().decode(charset),
        #                 keep_blank_values=True,
        #                 encoding=charset,
        #             )
        #         )

        # self._post = MultiDictProxy(out)
        # return self._post

##########################################################################################

# from fastapi import FastAPI, Request
# import typing
# import asyncio
# import time 
# import logging 

# Scope = typing.MutableMapping[str, typing.Any]
# Message = typing.MutableMapping[str, typing.Any]
# Receive = typing.Callable[[], typing.Awaitable[Message]]
# Send = typing.Callable[[Message], typing.Awaitable[None]]
# RequestTuple = typing.Tuple[Scope, Receive, Send]

# logger = logging.getLogger("uvicorn")

# async def very_heavy_lifting(requests: dict[int,RequestTuple], batch_no) -> dict[int, RequestTuple]:
#     #This mimics a heavy lifting function, takes a whole 3 seconds to process this batch
#     logger.info(f"Heavy lifting for batch {batch_no} with {len(requests.keys())} requests")
#     await asyncio.sleep(3)
#     processed_requests: dict[int,RequestTuple] = {}
#     for id, request in requests.items():
#         request[0]["heavy_lifting_result"] = f"result of request {id} in batch {batch_no}"
#         processed_requests[id] = (request[0], request[1], request[2])
#     return processed_requests

# class Batcher():
#     def __init__(self, batch_max_size: int = 5, batch_max_seconds: int = 3) -> None:
#         self.batch_max_size = batch_max_size
#         self.batch_max_seconds = batch_max_seconds
#         self.to_process: dict[int, RequestTuple] = {}
#         self.processing: dict[int, RequestTuple] = {}
#         self.processed: dict[int, RequestTuple] = {}
#         self.batch_no = 1

#     def start_batcher(self):
#         _ = asyncio.get_event_loop()
#         self.batcher_task = asyncio.create_task(self._batcher())

#     async def _batcher(self):
#         while True:
#             time_out = time.time() + self.batch_max_seconds
#             while time.time() < time_out:
#                 if len(self.to_process) >= self.batch_max_size:
#                     logger.info(f"Batch {self.batch_no} is full \
#                         (requests: {len(self.to_process.keys())}, max allowed: {self.batch_max_size})")
#                     self.batch_no += 1
#                     await self.process_requests(self.batch_no)

#                     break
#                 await asyncio.sleep(0)
#             else:
#                 if len(self.to_process)>0:
#                     logger.info(f"Batch {self.batch_no} is over timelimit (requests: {len(self.to_process.keys())})")
#                     self.batch_no += 1
#                     await self.process_requests(self.batch_no)
#             await asyncio.sleep(0)

#     async def process_requests(self, batch_no: int):
#         logger.info(f"Start of processing batch {batch_no}...")
#         for id, request in self.to_process.items():
#             self.processing[id] = request
#         self.to_process = {}
#         processed_requests  = await very_heavy_lifting(self.processing, batch_no)
#         self.processed = processed_requests
#         self.processing = {}
#         logger.info(f"Finished processing batch {batch_no}")

# batcher = Batcher() 

# class InterceptorMiddleware():
#     def __init__(self, app) -> None:
#         self.app = app
#         self.request_id: int = 0

#     async def __call__(self, scope: Scope, receive: Receive, send: Send):
#         if scope["type"] != "http":  # pragma: no cover
#             await self.app(scope, receive, send)
#             return

#         self.request_id += 1
#         current_id = self.request_id
#         batcher.to_process[self.request_id] = (scope, receive, send)
#         logger.info(f"Added request {current_id} to batch {batcher.batch_no}.")
#         while True:
#             request = batcher.processed.get(current_id, None)
#             if not request:
#                 await asyncio.sleep(0.5)
#             else:
#                 logger.info(f"Request {current_id} was processed, forwarding to FastAPI endpoint..")
#                 batcher.processed.pop(current_id)
#                 await self.app(request[0], request[1], request[2])
#                 await asyncio.sleep(0)

# app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     batcher.start_batcher()
#     return

# app.add_middleware(InterceptorMiddleware)

# @app.get("/")
# async def root(request: Request):
#     return {"Return value": request["heavy_lifting_result"]}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

