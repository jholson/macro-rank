#!/usr/bin/env python3
import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

from collections import namedtuple
Ranking = namedtuple('Ranking', 'name score columns')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'debug': True,
            'autoescape': None,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Expected incoming object format
        rankings = [
            Ranking(
                name = 'Jake',
                score = 5,
                columns = { }
            ),
            Ranking(
                name = 'Nipunn',
                score = 10,
                columns = {
                    'herp': 'text in the herp column',
                    'derp': 'text in the derp column',
                }
            ),
            Ranking(
                name = 'Robert',
                score = 2,
                columns = {
                    'derp': r'<img src="http://i.imgur.com/L3J6n.jpg" style="max-width: 100; height: auto;" />',
                    'foo': 'bar',
                }
            ),
        ]

        columns = set()
        for ranking in rankings:
            columns.update(ranking.columns)
        columns = sorted(list(columns))

        rows = []
        for ranking in sorted(rankings, key=lambda x: x.score, reverse=True):
            column_values = { column: ranking.columns[column] if column in ranking.columns else "" for column in columns }
            column_values['Name'] = ranking.name
            column_values['Score'] = ranking.score
            rows.append(column_values)

        self.render(
            'index.html',
            page_title = 'Title',
            columns = columns,
            rows = rows,
        )

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
