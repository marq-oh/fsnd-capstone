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
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjI1ODIwMSwiZXhwIjoxNTgyMjY1NDAxLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.E8C4Mvmvg6T2IYZl4hgE8V7uGQMijpeQqYe18vJ1-4PB17X0DO_YpPaUCdYRfGQ6uZm5Yz1Vlbl9H3PhAgBM-BXxEAN5TL_itUfhOD3vNPKuYakAfMwQS7kAMVryCr1EionL2sFl5uKBQGq-jJXSHen6EyLK976EH6JVcABKWwCafNoVGkgzSqTmIxPfMR1Ht1GB3b5IGyzWazdkAm5sxmMIhnvuWaEtOK50gXvRMKPCn9v17Vqf5wbRah47Eu_jYsVaRMGh7ndYre-U-GtGrzxuYKJbz46F2rCpBUV_ZXI3LmZcsy0qIvU-57BEWV9JNK8I4T52elf1QU60xGb6uw"
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to get specific movie with assistant token -> 405
    def test_get_movies_assistant_405(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjI1ODIwMSwiZXhwIjoxNTgyMjY1NDAxLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.E8C4Mvmvg6T2IYZl4hgE8V7uGQMijpeQqYe18vJ1-4PB17X0DO_YpPaUCdYRfGQ6uZm5Yz1Vlbl9H3PhAgBM-BXxEAN5TL_itUfhOD3vNPKuYakAfMwQS7kAMVryCr1EionL2sFl5uKBQGq-jJXSHen6EyLK976EH6JVcABKWwCafNoVGkgzSqTmIxPfMR1Ht1GB3b5IGyzWazdkAm5sxmMIhnvuWaEtOK50gXvRMKPCn9v17Vqf5wbRah47Eu_jYsVaRMGh7ndYre-U-GtGrzxuYKJbz46F2rCpBUV_ZXI3LmZcsy0qIvU-57BEWV9JNK8I4T52elf1QU60xGb6uw"
        res = self.client().get('/movies/1', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Test to insert movie with assistant token -> 403 (RBAC test for assistant)
    def test_insert_movie_assistant_403(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjI1ODIwMSwiZXhwIjoxNTgyMjY1NDAxLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.E8C4Mvmvg6T2IYZl4hgE8V7uGQMijpeQqYe18vJ1-4PB17X0DO_YpPaUCdYRfGQ6uZm5Yz1Vlbl9H3PhAgBM-BXxEAN5TL_itUfhOD3vNPKuYakAfMwQS7kAMVryCr1EionL2sFl5uKBQGq-jJXSHen6EyLK976EH6JVcABKWwCafNoVGkgzSqTmIxPfMR1Ht1GB3b5IGyzWazdkAm5sxmMIhnvuWaEtOK50gXvRMKPCn9v17Vqf5wbRah47Eu_jYsVaRMGh7ndYre-U-GtGrzxuYKJbz46F2rCpBUV_ZXI3LmZcsy0qIvU-57BEWV9JNK8I4T52elf1QU60xGb6uw"
        data = {
            "title": "New Movie Title",
            "release_date": "2020-04-01"
        }
        res = self.client().post('/movies', json=data, headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test to insert movie with director token -> 403 (RBAC test for director)
    def test_insert_movie_director_403(self):
        # Director Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MTMwMjc3NSwiZXhwIjoxNTgxMzA5OTc1LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.fG-Nxq_MkB_mH-BxcGomeDh7izIulOItJ7-lJ_HAvT7wYoqaZcwbvujr2ol96_6ztbZDjnOWVotZyp8oka1x2LCyJS_VNMVmJU_liGyzGs4BB4AHcpfCC2GF5f4Xxo-MgPD2asycOi6-c7pnnRbzPoqR_hFJB0W0CXK7gwNXCk7OE0THt0lVYALvkLSwn_v2SgYfewVDIj-ErA7LOGsYudQZwmhwfhM_PPgGzG4PjRYw03T3YCx8xQaM2Opv_4-zW9DceX8SR586_l8k358Hs2zCaMaCPmaroEIhF4KMTZ67TseSx2EFzx5TwTpE4zgzd1T5LKT6-tMKgYD6mZnS6A"
        data = {
            "title": "New Movie Title",
            "release_date": "2020-04-01"
        }
        res = self.client().post('/movies', json=data, headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test to insert movie with producer token -> 200 (RBAC test for producer)
    def test_insert_movie_producer_200(self):
        # Producer Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMWEzZjBjZjMwMWEyMGNjN2Q0NjlmMCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MTkwMjkzOCwiZXhwIjoxNTgxOTEwMTM4LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50IiwicG9zdDptb3ZpZSJdfQ.LvSS_untVdwMTgt99a3EAUrZ_a8j8qncf9-zlW2AfH9eQkrmxF5ud7Joaeoefl9th7cI_jMoHXiGi7BuYQU1DoY5inTcpO-uV5Axkgo9S9ajz0w1ktuXgTtBxmnFIMjT-ZMqoSJujxM2m5_FafllK65rmIqyg_An2o6tGen2Oubz8UjLUX9XRVeCY_cIy9GpP4zWkXgEKO3htS_U_SNBdh4gwWKV1jyoX0Lzg-xktfUsul_9Oj22ojzg__QyobUnHSaoMZ7kmLGXuyq0GHGkRNByI-plEutHQNXpB4j4mFPcoJnCvCnN2ZnMBBOpxE2WZ0SWMcyVV5HN-UBmmCZi8w"
        data = {
            "title": "New Movie Title",
            "release_date": "2020-04-01"
        }
        res = self.client().post('/movies', json=data, headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test to get all actors with assistant token -> 200
    def test_get_actors_assistant_200(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjI1ODIwMSwiZXhwIjoxNTgyMjY1NDAxLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.E8C4Mvmvg6T2IYZl4hgE8V7uGQMijpeQqYe18vJ1-4PB17X0DO_YpPaUCdYRfGQ6uZm5Yz1Vlbl9H3PhAgBM-BXxEAN5TL_itUfhOD3vNPKuYakAfMwQS7kAMVryCr1EionL2sFl5uKBQGq-jJXSHen6EyLK976EH6JVcABKWwCafNoVGkgzSqTmIxPfMR1Ht1GB3b5IGyzWazdkAm5sxmMIhnvuWaEtOK50gXvRMKPCn9v17Vqf5wbRah47Eu_jYsVaRMGh7ndYre-U-GtGrzxuYKJbz46F2rCpBUV_ZXI3LmZcsy0qIvU-57BEWV9JNK8I4T52elf1QU60xGb6uw"
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to get specific actor with assistant token -> 405
    def test_get_actors_assistant_405(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjI1ODIwMSwiZXhwIjoxNTgyMjY1NDAxLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.E8C4Mvmvg6T2IYZl4hgE8V7uGQMijpeQqYe18vJ1-4PB17X0DO_YpPaUCdYRfGQ6uZm5Yz1Vlbl9H3PhAgBM-BXxEAN5TL_itUfhOD3vNPKuYakAfMwQS7kAMVryCr1EionL2sFl5uKBQGq-jJXSHen6EyLK976EH6JVcABKWwCafNoVGkgzSqTmIxPfMR1Ht1GB3b5IGyzWazdkAm5sxmMIhnvuWaEtOK50gXvRMKPCn9v17Vqf5wbRah47Eu_jYsVaRMGh7ndYre-U-GtGrzxuYKJbz46F2rCpBUV_ZXI3LmZcsy0qIvU-57BEWV9JNK8I4T52elf1QU60xGb6uw"
        res = self.client().get('/actors/1', headers={'Authorization': 'Bearer ' + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Test to insert actor with assistant token -> 403 (RBAC test for assistant)
    def test_insert_actor_assistant_403(self):
        # Assistant Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MjI1ODIwMSwiZXhwIjoxNTgyMjY1NDAxLCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.E8C4Mvmvg6T2IYZl4hgE8V7uGQMijpeQqYe18vJ1-4PB17X0DO_YpPaUCdYRfGQ6uZm5Yz1Vlbl9H3PhAgBM-BXxEAN5TL_itUfhOD3vNPKuYakAfMwQS7kAMVryCr1EionL2sFl5uKBQGq-jJXSHen6EyLK976EH6JVcABKWwCafNoVGkgzSqTmIxPfMR1Ht1GB3b5IGyzWazdkAm5sxmMIhnvuWaEtOK50gXvRMKPCn9v17Vqf5wbRah47Eu_jYsVaRMGh7ndYre-U-GtGrzxuYKJbz46F2rCpBUV_ZXI3LmZcsy0qIvU-57BEWV9JNK8I4T52elf1QU60xGb6uw"
        data = {
            "name": "New Actor Name",
            "age": "25",
            "gender": "M"
        }
        res = self.client().post('/actors', json=data, headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test to insert actor with director token -> 200 (RBAC test for director)
    def test_insert_actor_director_200(self):
        # Director Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNDBjMzc1ODllNmM0MGU3ZDczNjEyYiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MTMwMjc3NSwiZXhwIjoxNTgxMzA5OTc1LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50Il19.fG-Nxq_MkB_mH-BxcGomeDh7izIulOItJ7-lJ_HAvT7wYoqaZcwbvujr2ol96_6ztbZDjnOWVotZyp8oka1x2LCyJS_VNMVmJU_liGyzGs4BB4AHcpfCC2GF5f4Xxo-MgPD2asycOi6-c7pnnRbzPoqR_hFJB0W0CXK7gwNXCk7OE0THt0lVYALvkLSwn_v2SgYfewVDIj-ErA7LOGsYudQZwmhwfhM_PPgGzG4PjRYw03T3YCx8xQaM2Opv_4-zW9DceX8SR586_l8k358Hs2zCaMaCPmaroEIhF4KMTZ67TseSx2EFzx5TwTpE4zgzd1T5LKT6-tMKgYD6mZnS6A"
        data = {
            "name": "New Actor Name",
            "age": "25",
            "gender": "M"
        }
        res = self.client().post('/actors', json=data, headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to insert assignment with producer token -> 200 (RBAC test for producer)
    def test_insert_assignment_producer_200(self):
        # Producer Token
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMWEzZjBjZjMwMWEyMGNjN2Q0NjlmMCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MTkwMjkzOCwiZXhwIjoxNTgxOTEwMTM4LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50IiwicG9zdDptb3ZpZSJdfQ.LvSS_untVdwMTgt99a3EAUrZ_a8j8qncf9-zlW2AfH9eQkrmxF5ud7Joaeoefl9th7cI_jMoHXiGi7BuYQU1DoY5inTcpO-uV5Axkgo9S9ajz0w1ktuXgTtBxmnFIMjT-ZMqoSJujxM2m5_FafllK65rmIqyg_An2o6tGen2Oubz8UjLUX9XRVeCY_cIy9GpP4zWkXgEKO3htS_U_SNBdh4gwWKV1jyoX0Lzg-xktfUsul_9Oj22ojzg__QyobUnHSaoMZ7kmLGXuyq0GHGkRNByI-plEutHQNXpB4j4mFPcoJnCvCnN2ZnMBBOpxE2WZ0SWMcyVV5HN-UBmmCZi8w"
        data = {
            "movie_id": 1,
            "actor_id": 1,
        }
        res = self.client().post('/assignments', json=data, headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()