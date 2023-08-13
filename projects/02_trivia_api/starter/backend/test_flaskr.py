import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://allen:plumbflo22!@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'what is the average velocity of a sparrow?',
            'answer': '5000 miles per hour',
            'category': '1',
            'difficulty': '3'
            }    

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    


    def tearDown(self):
        """Executed after reach test"""
        pass

        """
        TODO
        Write at least one test for each test for successful operation and for expected errors.
        """

   # categories  all
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    
    #get questions
 
    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    #create question

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

 
    #delete question - test fails if id does not exist
    def test_delete_question(self):
        res = self.client().delete("/questions/14")
        print(res.data)
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 14).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 14)
        self.assertEqual(question, None)
   
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


   #search question

    #get category questions

    # post quizzes


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()