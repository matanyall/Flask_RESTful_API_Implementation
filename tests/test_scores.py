from pyarcade_rest import app, db, User
import unittest
import json


class ScoresAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.db.drop_all()
        self.db.create_all()
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()

    def test_score_empty_response(self):
        response = self.app.get('/api/v1/scores/1')
        scores = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(scores), )

    def test_can_create_score(self):
        response = self.app.post(
            '/api/v1/scores/1',
            data=json.dumps({"game_name": "mastermind", "value": 10.0}),
            content_type='application/json'
        )
        score = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("mastermind", score["game_name"])
        self.assertEqual(10.0, score["value"])

    def test_can_read_scores(self):
        # Create two scores
        self.app.post(
            '/api/v1/scores/1',
            data=json.dumps({"game_name": "mastermind", "value": 10.0}),
            content_type='application/json'
        )

        self.app.post(
            '/api/v1/scores/1',
            data=json.dumps({"game_name": "connect_4", "value": 30.0}),
            content_type='application/json'
        )

        response = self.app.get('/api/v1/scores/1')
        scores = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(scores), 2)
        self.assertEqual(scores[0]["game_name"], "mastermind")
        self.assertEqual(scores[0]["value"], 10.0)
        self.assertEqual(scores[1]["game_name"], "connect_4")
        self.assertEqual(scores[1]["value"], 30.0)
        self.assertEqual(len(scores), 2)





