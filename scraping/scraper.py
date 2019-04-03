import os
import shelve
from urllib.request import urlopen
from inscriptis import get_text
from bs4 import BeautifulSoup

from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse


from distutils.dir_util import mkpath


app = Flask(__name__)
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("web_scraper.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def load_page(url):
    response = urlopen(url)
    page_contents = response.read().decode('utf-8')
    return page_contents


class TextScraper(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        websites = []

        for key in keys:
            websites.append(shelf[key])

        return {'message': 'Success', 'data': websites}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('url', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args
        url = request.get_json()
        print(url['url'])
        page_text = get_text(load_page(url['url']))
        file_name = url['url'].split('/')[2]
        scraped_text_path = '/tmp/' + file_name + '.txt'
        with open(scraped_text_path, 'w') as file:
            file.write(page_text)

        return {'message': 'Text_scraped', 'data': args}, 201


class ImagesScrapper(Resource):
    def get(self):
        website = request.get_json()
        return {'data': website}, 200

    def post(self):
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


api.add_resource(TextScraper, '/api/scrape_text')
api.add_resource(ImagesScrapper, '/api/scrape_image')


