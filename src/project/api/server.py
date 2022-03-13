import json

from sqlalchemy.exc import IntegrityError
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, HTTPError

from project.database.crud import select_entry, insert_entry, update_entry, delete_entry, select_entries
from project.database.models.request_info import RequestInfo
from project.utils.utils import bytes_to_json, base64_json


class AddHandler(RequestHandler):
    async def post(self):
        decoded_body = bytes_to_json(self.request.body)
        body_key = base64_json(decoded_body)
        existing_request: RequestInfo = await select_entry(RequestInfo, body_key)
        if not existing_request:
            existing_request = await insert_entry(RequestInfo, id=body_key, request=decoded_body)
        else:
            duplicates = existing_request.duplicates
            duplicates += 1
            await update_entry(existing_request, duplicates=duplicates)
        self.write(existing_request.id)


class GetHandler(RequestHandler):
    async def get(self):
        body_key = self.get_argument('key')
        existing_request_info: RequestInfo = await select_entry(RequestInfo, body_key)
        if not existing_request_info:
            raise HTTPError(status_code=404, log_message=f"{body_key} not found")
        response = json.dumps({"request_body": existing_request_info.request,
                               "duplicates": existing_request_info.duplicates})
        self.write(response)


class RemoveHandler(RequestHandler):
    async def delete(self):
        body_key = self.get_argument('key')
        existing_request_info: RequestInfo = await select_entry(RequestInfo, body_key)
        if not existing_request_info:
            raise HTTPError(status_code=404, log_message=f"{body_key} not found")
        await delete_entry(existing_request_info)


class UpdateHandler(RequestHandler):
    async def put(self):
        decoded_body = bytes_to_json(self.request.body)
        old_key = decoded_body.get('key')
        new_body = decoded_body.get('body')
        existing_request_info: RequestInfo = await select_entry(RequestInfo, old_key)
        if not existing_request_info:
            raise HTTPError(status_code=404, log_message=f"{old_key} not found")
        else:
            new_key = base64_json(new_body)
            if not old_key == new_key:
                try:
                    await update_entry(
                        existing_request_info,
                        id=new_key,
                        request=new_body,
                        duplicates=0

                    )
                except IntegrityError:
                    raise HTTPError(status_code=400, log_message=f"body already exist")
            else:
                raise HTTPError(status_code=400, log_message=f"request body is already up-to-date")


class StatisticHandler(RequestHandler):
    async def get(self):
        existing_requests_info = await select_entries(RequestInfo)
        request_info: RequestInfo
        duplicated_requests = len([True for request_info in existing_requests_info if request_info.duplicates > 0])
        self.write(f"Duplicated requests % is {duplicated_requests*100/len(existing_requests_info)}")


app = Application([
    (r"/api/add", AddHandler),
    (r"/api/get", GetHandler),
    (r"/api/remove", RemoveHandler),
    (r"/api/update", UpdateHandler),
    (r"/api/statistic", StatisticHandler),
])
app.listen(8888)
IOLoop.current().start()

# {"z": 1, "b": {"t": 4, "m":6, "a":4}, "t": 12}
# {"t": 12, "b": {"t": 4, "m":6, "a":4}, "z": 1}
#{"key": "IntcImJcIjoge1wiYVwiOiA0LCBcIm1cIjogNiwgXCJ0XCI6IDR9LCBcInRcIjogMTIsIFwielwiOiAxfSI=","body": {"t": 12, "b": {"t": 4, "m": 6, "a": 4}, "z": 1}}
#{"key": "IntcImJcIjoge1wiYVwiOiA0LCBcIm1cIjogNiwgXCJ0XCI6IDR9LCBcInRcIjogMTIsIFwielwiOiAxfSI=","body": {"y": 12, "a": {"t": 4666, "m": 6555, "c": 4}, "g": 1223}}
# {"y": 12, "a": {"t": 4666, "m":6555, "c":4}, "g": 1223}