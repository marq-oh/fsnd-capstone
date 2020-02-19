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
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMWEzZjBjZjMwMWEyMGNjN2Q0NjlmMCIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MTkwMjkzOCwiZXhwIjoxNTgxOTEwMTM4LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOmFzc2lnbm1lbnQiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFzc2lnbm1lbnRzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDphc3NpZ25tZW50IiwicG9zdDptb3ZpZSJdfQ.LvSS_untVdwMTgt99a3EAUrZ_a8j8qncf9-zlW2AfH9eQkrmxF5ud7Joaeoefl9th7cI_jMoHXiGi7BuYQU1DoY5inTcpO-uV5Axkgo9S9ajz0w1ktuXgTtBxmnFIMjT-ZMqoSJujxM2m5_FafllK65rmIqyg_An2o6tGen2Oubz8UjLUX9XRVeCY_cIy9GpP4zWkXgEKO3htS_U_SNBdh4gwWKV1jyoX0Lzg-xktfUsul_9Oj22ojzg__QyobUnHSaoMZ7kmLGXuyq0GHGkRNByI-plEutHQNXpB4j4mFPcoJnCvCnN2ZnMBBOpxE2WZ0SWMcyVV5HN-UBmmCZi8w"
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

    def test_get_movies_assistant(self):
        #jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTXpOMEZCUXpoRFJERXpORVZEUkRBeE9VWXlOa00yTkRSRVJEZ3hPRGxFTnpORU9FUTFOZyJ9.eyJpc3MiOiJodHRwczovL3N0dWRlbnQtbXNqLTUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMTZhZDIwYTE5Njk3MGVlMDNlOGVlMyIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4MTkwMjU4NiwiZXhwIjoxNTgxOTA5Nzg2LCJhenAiOiJZc0t4anZjMDZXd3kwUHoxcW5RRnNVUGlPeXhZZGFJcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphc3NpZ25tZW50cyIsImdldDptb3ZpZXMiXX0.UhVUtScqk6oJ5959zyIaQrnyFZjgsVmElJ2Hsz3czz71QO-cA12SLP5kT2GIAbvqDd9qrELMls7zVl1I-tk5i94BxnbhTXu7_vdftNmOFBR5JnNQeZ5fdl0nQaWbbGGfaEW5Eyrj_slcH59J4OTswNW0uzR1W537t2IAag9OhWO6SXS66pOeoVLzijc-VzD0SiS0cs2xBn8IVpTYa2Z0aNMrBJgAMmdY8G0QFxzvZhYg1RmlanCuI1qvuPqM6cLnx1qLYM5QDNVXiZ_Be6Y6oft4wUjsJQv0PBq_fBRmNZRCoijAS-l2rH5jYmgcJzPvWneecbyFad-sgBayZVPRmQ'
        # res = self.client().get('/movies')
        res = self.client().get('/movies', headers={'Authorization': self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''
    def test_get_movies_405(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
    '''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()