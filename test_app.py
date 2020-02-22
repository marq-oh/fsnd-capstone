import os
import unittest
import dateutil.parser
import json

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors, Assignments
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from auth import AuthError, requires_auth
from random import random
from datetime import date

class TestCases(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('postgres:marco@localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test to get all movies with assistant token -> 200
    def test_get_movies_assistant_200(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2JjZjQ0OWZlMGQ0YjkyZGM4NCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwOTc3NSwiZXhwIjoxNTgyNDE2OTc1LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphc3NpZ25tZW50cyIsImdldDptb3ZpZXMiXX0.FPcSXNHfa7z2HD1iMwxc2AHm6QejAWMvEcnQjae3BfvWJELyEYU3bBUY-GdV9oheuBf8ck0kybeTbCI_1ZwNcSQkSTSGLIbEIgeNf0_rtSOnEvame-pP6up2hH90m7yOgeDY9PqcNm3bcZMEUTxgGkF2wWflZZnZLZWjxqkoeIpRyB8hvDadBKw3laUFXy-N0UASTP6y1BhjLMVRq1CVzx1Jw1pHFXR9tNTgI-aXlODPbUnQbnWyZIu4lLv7NL7CgbySI6O_nO3408VoCtLgwjSXZIVkEWEIZOyYujdwz946yf4av-UEFLu3PYRcOZZijexhPu3kOgay9czIMrujjg"
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to get specific movie with assistant token -> 405
    def test_get_movies_assistant_405(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMTZhZDIwYTE5Njk3MGVlMDNlOGVlMyIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwMzY3MSwiZXhwIjoxNTgyNDEwODcxLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphc3NpZ25tZW50cyIsImdldDptb3ZpZXMiXX0.MglfohvJG6AxqXjdCelvtGS4C7P30PapryzWOTaVuWKba_GfQDWEEzYEEa8MHR7_P5aoI6Lj8GfQq78YOqPvkTX6K0WXW0k5qYCbCWNQ0hjOsRQJPpdcgrdrUrWbmDBXf1Pv4UpuFPxfDU15tFI33yc4R2ESQq-nSLC4y8w4aniYsUOpqMBY1YamtTkNCk_UBLEqR1cn5lii4m4HybQkbQdwG3lwM56W-m2RuByqNhFLwYkwvMs1sdaomMAEQyuUK7Ckk3wH04EVHrt-lwWq1CcJ1oCgcLBEg5cMNPos0eHkZNh5SpTdAFMMHVzuoT4BxU5cGOUW8xtpn3hBUkbdxg"
        res = self.client().get('/movies/1', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Test to insert movie with assistant token -> 401 (RBAC test for assistant)
    def test_insert_movie_assistant_403(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2JjZjQ0OWZlMGQ0YjkyZGM4NCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwOTc3NSwiZXhwIjoxNTgyNDE2OTc1LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphc3NpZ25tZW50cyIsImdldDptb3ZpZXMiXX0.FPcSXNHfa7z2HD1iMwxc2AHm6QejAWMvEcnQjae3BfvWJELyEYU3bBUY-GdV9oheuBf8ck0kybeTbCI_1ZwNcSQkSTSGLIbEIgeNf0_rtSOnEvame-pP6up2hH90m7yOgeDY9PqcNm3bcZMEUTxgGkF2wWflZZnZLZWjxqkoeIpRyB8hvDadBKw3laUFXy-N0UASTP6y1BhjLMVRq1CVzx1Jw1pHFXR9tNTgI-aXlODPbUnQbnWyZIu4lLv7NL7CgbySI6O_nO3408VoCtLgwjSXZIVkEWEIZOyYujdwz946yf4av-UEFLu3PYRcOZZijexhPu3kOgay9czIMrujjg"
        data = {
            "title": "New Movie Title",
            "release_date": "2020-04-01"
        }
        res = self.client().post('/movies', json=data, headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test to insert movie with director token -> 403 (RBAC test for director)
    def test_insert_movie_director_403(self):
        # Director Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2UwZjQ0OWZlMGQ0YjkyZGM4YiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwOTE2MCwiZXhwIjoxNTgyNDE2MzYwLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.zfVrmJhI9zCHLyduLX-c36siUlTTyhGVqBCkYGiAz6P14F8Oys0DHgS9Av5oTge5pkmmJYGqb-2WyBch_U9-NyDzAkQjeoviqtscRo9djIQo4NPZfTRwXs_u-gZWb3NMBj1OUEYTyA25eA33SJRt4fKbpWUGodWGQDWAI5O9dyMy1Te5kXGRkO4H7yW-IdplI7Tgv4K8t5vX7dzKf3mK__Gpp8tbMynkvjPHsn4m2hEge_vxbyKMWqY1CSOAGwLsdCeVCmw-d4c0WLBrGl_o925Dkk78iJ83CZ0qb2aTARhTi_op0bdKFuXyI6LA4FlGw4r2OXeikT-GSRc_-Bg2ZQ"
        data = {
            "title": "New Movie Title",
            "release_date": "2020-04-01"
        }
        res = self.client().post('/movies', json=data, headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test to insert movie with producer token -> 200 (RBAC test for producer)
    def test_insert_movie_producer_200(self):
        # Producer Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2YyZjQ0OWZlMGQ0YjkyZGM4ZSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwODI2NCwiZXhwIjoxNTgyNDE1NDY0LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50IiwicG9zdDptb3ZpZSJdfQ.HM4p0X3O9HTTy-mUPtH7Cao6q1ZcpY4bIv18F76PSiEaNgJ6eJD2P_nhyMEoWBhRVMXWJIrT4hw0RaFT7UTbtsbc0HKuusj6_R7rrgzCDUPsH6gM3seZU3gUhYrzKAJLwz95UE_MvzPnGLkoAIEx6-zZisws14tgiMzTKmcTMaAxLegIrJxBR0p1QDLaVIwRW18zSoJuQ4kwoFid3juT0wq6LuSa0cYkHwNb-XtPtn1KyOYG-webNCY71IfmeNNYE8V7CpZSV6tBaT-Tmg4LTY7RIzx1SoiroM5jRiBeIAgT1Awb1iK3xHxnP2H4diuhov1btx_6smAHY8vHi0IR7g"
        movie_title = "New Movie Title" + str(random())
        data = {
            "title": movie_title,
            "release_date": date.today()
        }
        res = self.client().post('/movies', json=data, headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to get all actors with assistant token -> 200
    def test_get_actors_assistant_200(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2JjZjQ0OWZlMGQ0YjkyZGM4NCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwOTc3NSwiZXhwIjoxNTgyNDE2OTc1LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphc3NpZ25tZW50cyIsImdldDptb3ZpZXMiXX0.FPcSXNHfa7z2HD1iMwxc2AHm6QejAWMvEcnQjae3BfvWJELyEYU3bBUY-GdV9oheuBf8ck0kybeTbCI_1ZwNcSQkSTSGLIbEIgeNf0_rtSOnEvame-pP6up2hH90m7yOgeDY9PqcNm3bcZMEUTxgGkF2wWflZZnZLZWjxqkoeIpRyB8hvDadBKw3laUFXy-N0UASTP6y1BhjLMVRq1CVzx1Jw1pHFXR9tNTgI-aXlODPbUnQbnWyZIu4lLv7NL7CgbySI6O_nO3408VoCtLgwjSXZIVkEWEIZOyYujdwz946yf4av-UEFLu3PYRcOZZijexhPu3kOgay9czIMrujjg"
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to get specific actor with assistant token -> 405
    def test_get_actors_assistant_405(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2JjZjQ0OWZlMGQ0YjkyZGM4NCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwOTc3NSwiZXhwIjoxNTgyNDE2OTc1LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphc3NpZ25tZW50cyIsImdldDptb3ZpZXMiXX0.FPcSXNHfa7z2HD1iMwxc2AHm6QejAWMvEcnQjae3BfvWJELyEYU3bBUY-GdV9oheuBf8ck0kybeTbCI_1ZwNcSQkSTSGLIbEIgeNf0_rtSOnEvame-pP6up2hH90m7yOgeDY9PqcNm3bcZMEUTxgGkF2wWflZZnZLZWjxqkoeIpRyB8hvDadBKw3laUFXy-N0UASTP6y1BhjLMVRq1CVzx1Jw1pHFXR9tNTgI-aXlODPbUnQbnWyZIu4lLv7NL7CgbySI6O_nO3408VoCtLgwjSXZIVkEWEIZOyYujdwz946yf4av-UEFLu3PYRcOZZijexhPu3kOgay9czIMrujjg"
        res = self.client().get('/actors/1', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Test to insert actor with assistant token -> 401 (RBAC test for assistant)
    def test_insert_actor_assistant_403(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2JjZjQ0OWZlMGQ0YjkyZGM4NCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwOTc3NSwiZXhwIjoxNTgyNDE2OTc1LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphc3NpZ25tZW50cyIsImdldDptb3ZpZXMiXX0.FPcSXNHfa7z2HD1iMwxc2AHm6QejAWMvEcnQjae3BfvWJELyEYU3bBUY-GdV9oheuBf8ck0kybeTbCI_1ZwNcSQkSTSGLIbEIgeNf0_rtSOnEvame-pP6up2hH90m7yOgeDY9PqcNm3bcZMEUTxgGkF2wWflZZnZLZWjxqkoeIpRyB8hvDadBKw3laUFXy-N0UASTP6y1BhjLMVRq1CVzx1Jw1pHFXR9tNTgI-aXlODPbUnQbnWyZIu4lLv7NL7CgbySI6O_nO3408VoCtLgwjSXZIVkEWEIZOyYujdwz946yf4av-UEFLu3PYRcOZZijexhPu3kOgay9czIMrujjg"
        data = {
            "name": "New Actor Name",
            "age": "25",
            "gender": "M"
        }
        res = self.client().post('/actors', json=data, headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test to insert actor with director token -> 200 (RBAC test for director)
    def test_insert_actor_director_200(self):
        # Director Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2UwZjQ0OWZlMGQ0YjkyZGM4YiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwOTE2MCwiZXhwIjoxNTgyNDE2MzYwLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.zfVrmJhI9zCHLyduLX-c36siUlTTyhGVqBCkYGiAz6P14F8Oys0DHgS9Av5oTge5pkmmJYGqb-2WyBch_U9-NyDzAkQjeoviqtscRo9djIQo4NPZfTRwXs_u-gZWb3NMBj1OUEYTyA25eA33SJRt4fKbpWUGodWGQDWAI5O9dyMy1Te5kXGRkO4H7yW-IdplI7Tgv4K8t5vX7dzKf3mK__Gpp8tbMynkvjPHsn4m2hEge_vxbyKMWqY1CSOAGwLsdCeVCmw-d4c0WLBrGl_o925Dkk78iJ83CZ0qb2aTARhTi_op0bdKFuXyI6LA4FlGw4r2OXeikT-GSRc_-Bg2ZQ"
        data = {
            "name": "New Actor Name",
            "age": "25",
            "gender": "M"
        }
        res = self.client().post('/actors', json=data, headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to insert assignment with producer token -> 200 (RBAC test for producer)
    def test_insert_assignment_producer_200(self):
        # Producer Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNTE1Y2YyZjQ0OWZlMGQ0YjkyZGM4ZSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjQwODI2NCwiZXhwIjoxNTgyNDE1NDY0LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50IiwicG9zdDptb3ZpZSJdfQ.HM4p0X3O9HTTy-mUPtH7Cao6q1ZcpY4bIv18F76PSiEaNgJ6eJD2P_nhyMEoWBhRVMXWJIrT4hw0RaFT7UTbtsbc0HKuusj6_R7rrgzCDUPsH6gM3seZU3gUhYrzKAJLwz95UE_MvzPnGLkoAIEx6-zZisws14tgiMzTKmcTMaAxLegIrJxBR0p1QDLaVIwRW18zSoJuQ4kwoFid3juT0wq6LuSa0cYkHwNb-XtPtn1KyOYG-webNCY71IfmeNNYE8V7CpZSV6tBaT-Tmg4LTY7RIzx1SoiroM5jRiBeIAgT1Awb1iK3xHxnP2H4diuhov1btx_6smAHY8vHi0IR7g"
        data = {
            "movie_id": 2,
            "actor_id": 2,
        }
        res = self.client().post('/assignments', json=data, headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()