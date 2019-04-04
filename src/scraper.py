from urllib.request import urlopen
from inscriptis import get_text
from bs4 import BeautifulSoup

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

# from .storage import models

app = Flask(__name__)

api = Api(app)


class Storage(Resource):
    # get request for poending
    def get(self):
        parser = reqparse.RequestParser()

        url = parser.add_argument('url', required=True)
        text = parser.add_argument('text', required=True)
        image = parser.add_argument('image', required=True)

        args = parser.parse_args()
        # here should be insert into db pending requests
        # should be error handling
        # models.parse_request.insert().values(url=url, text=text, image=image)
        return {'message': 'inserted',
                'data': args}, 200


def load_page(url):
    # get html
    response = urlopen(url)
    page_contents = response.read().decode('utf-8')
    return page_contents


class TextParser(Resource):
    # parse text and download file
    def post(self):
        url = request.get_json()
        page_text = get_text(load_page(url['url']))
        file_name = url['url'].split('/')[2]
        scraped_text_path = '/tmp/' + file_name + '.txt'
        # models.parse_request.insert().values(parse_request_id=parse_request_id, content=content)
        with open(scraped_text_path, 'w') as file:
            file.write(page_text)
        # should be error handling

        return {'success': f'Text parsed into {scraped_text_path}'}, 201


class ImageParser(Resource):
    # parse images and download
    def post(self):
        url = request.get_json()
        soup_data = BeautifulSoup(load_page(url['url']), "html.parser")
        images = soup_data.findAll('img')
        # should be Celery for asynchronous tasks
        for img in images:
            temp = img.get('src')
            if temp[0] == '/':
                image = 'https://' + url['url'].split('/')[2] + temp
                if temp[1] == '/':
                    image = 'https:' + temp
            else:
                image = temp
            print(image)
            file_number = 1
            nametemp = f"{url['url'].split('/')[2]}_" + img.get('alt')
            if len(nametemp) == 0:
                filename = str(file_number)
                file_number += 1
            else:
                filename = nametemp

            try:
                with open(f'/tmp/{filename}.jpg', 'wb') as file:
                    file.write(urlopen(image).read())
            except Exception as e:
                print(e, image)
                # continue  parsing website if img url failed 
                continue
        return {'success': 'Images parsed into tmp catalogue'}, 201


api.add_resource(TextParser, '/api/persist_text')
api.add_resource(ImageParser, '/api/persist_image')
api.add_resource(Storage, '/api/queue_request')


