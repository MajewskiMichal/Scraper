from urllib.request import urlopen
from inscriptis import get_text
from bs4 import BeautifulSoup

from flask import Flask, request, g
from flask_celery import make_celery
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'web_scraper.db'
celery = make_celery(app)

api = Api(app)


class AbstractParser:

    def __init__(self, url):
        self.url = url

    def load_page(self):
        response = urlopen(self.url)
        page_contents = response.read().decode('utf-8')
        return page_contents


class TextParser(Resource):

    def get(self):
        return {'message': 'Success', 'data': websites}, 200

    def perstist_text(self):

        url = request.get_json()
        print(url['url'])
        page_text = get_text(load_page(url['url']))
        file_name = url['url'].split('/')[2]
        scraped_text_path = '/tmp/' + file_name + '.txt'
        with open(scraped_text_path, 'w') as file:
            file.write(page_text)

        return {'message': 'Text_scraped', 'data': args}, 201


class ImageParser(Resource):
    def get(self):
        website = request.get_json()
        return {'data': website}, 200

    def persist_image(self):
        url = request.get_json()
        print(url)
        soup_data = BeautifulSoup(load_page(url['url']), "html.parser")
        images = soup_data.findAll('img')
        # id = uuid.
        # nowy watek wspolbierzny (selery)
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
                with open(f'images/{filename}.jpg', 'wb') as file:
                    file.write(urlopen(image).read())
            except Exception as e:
                print(e, image)
                continue
        return {'success': 'test'}, 201


api.add_resource(TextParser, '/api/scrape_text')
api.add_resource(ImageParser, '/api/scrape_image')


