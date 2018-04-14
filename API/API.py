import tornado.ioloop
import tornado.web
import API.DataLoader as DataLoader
import threading
import os
import API.ModelTrainer as ModelTrainer
# import secrets
# import numpy as np
# import argparse
import json
# import random
# import string
# import webbrowser
# import requests

# Global vars, mutable type, to be updated by threads
root = os.path.dirname(__file__)
haveData = [False]
dataLoading = [False]
haveModel = [False]
modelLoading = [False]
dataSource = [None]
models = [None]


class PostData(tornado.web.RequestHandler):
    def get(self):
        self.redirect("..")

    def post(self):
        file = self.request.files['input_file'][0]
        # spawn thread to handle file saving
        t = threading.Thread(target=DataLoader.savefile, args=(file, haveData, dataLoading, dataSource))
        t.start()
        dataLoading[0] = True
        self.redirect("..")


class GetColumns(tornado.web.RequestHandler):
    def get(self):
        this_file = os.path.join(root, dataSource[0])
        with open(this_file) as f:
            lines = [line.split("|") for line in f][0]
            lines = [val.replace("\n", "") for val in lines]
        self.write(json.dumps({"Values": lines}))


# TODO  With selected list of columns, train model, write to models
# TODO  This should be threaded and report result to modelLoading and haveModel
class TrainModel(tornado.web.RequestHandler):
    def get(self):
        target_col = self.get_arguments("target")
        data_cols = self.get_arguments("fields").split(",")
        if dataSource[0] is not None:
            this_file = os.path.join(root, dataSource[0])
            t = threading.Thread(target=ModelTrainer.trainStart,
                                 args=(this_file, target_col, data_cols, modelLoading, haveModel, models))
            t.start()

            self.set_status(200)
            self.write(json.dumps({"lol": "Lmao"}))
        else:
            self.set_status(500)
            self.write(json.dumps({"Error": "No Data to train on."}))


# TODO Requires trained model to find optimal solution subject to some constraints
class Optimize(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps({"lol": "Lmao"}))


# TODO  Delete data and set haveData to false
class ClearDataCache(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps({"lol": "Lmao"}))


class DataLoadingCheck(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.write(json.dumps({"dataLoading": dataLoading[0]}))


class HaveDataCheck(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.write(json.dumps({"haveData:": haveData[0]}))


class ModelLoadingCheck(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.write(json.dumps({"modelLoading": modelLoading[0]}))


class HaveModelCheck(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.write(json.dumps({"haveModel": haveModel[0]}))


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/modelLoading", ModelLoadingCheck),
        (r"/haveModel", HaveModelCheck),
        (r"/haveData", HaveDataCheck),
        (r"/dataLoading", DataLoadingCheck),
        (r"/upload", PostData),
        (r"/columns", GetColumns),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
    ],
        template_path=os.path.join(root, 'templates'),
        static_path=os.path.join(root, 'static')
    )



if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

