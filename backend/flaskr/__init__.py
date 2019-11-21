import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from helpers import pagination


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """
            Use the after_request decorator to set 
            Access-Control-Allow.
        """
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PUT, DELETE, OPTIONS')
        return response

    @app.route("/categories")
    def categories():
        """
           Handles GET requests for all available
           categories.
           returns:
           - all categories
        """
        data = []
        categories = Category.query.all()
        for category in categories:
            data.append(category.type)
        return jsonify({
            "categories": data
        }), 200

    # todo, add next and prev links for pagination...
    @app.route("/questions")
    def get_questions():
        """
            Handles GET requests for questions categories,
            including pagination.
            returns:
            - a list of questions
            - total number of questions
            - current category
            - categories
        """
        page = request.args.get('page', 1, type=int)
        questions = Question.query.join(
            Category, Category.id == Question.category).add_columns(
            Category.type).all()
        paginated_results = pagination(page, questions)
        categories = []
        for item in Category.query.all():
            categories.append(item.type)
        return jsonify({
            "categories": categories,
            "current_category": "all",
            "questions": paginated_results,
            "total_questions": len(questions),
        }), 200

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        """
            Handles DELETE requests for questions.
            params:
            - question id
            returns:
            - success message
        """
        question = Question.query.filter_by(id=question_id).first()
        if question:
            question.delete()
            return jsonify({
                "message": "Question successfully deleted."
            }), 200
        return jsonify({"message": "Question not found."})

    # add validation for exisiting questions
    @app.route("/questions", methods=["POST"])
    def create_question():
        """
            Handles POST requests for questions.
            returns:
            - question object
            - success message
        """
        body = request.get_json()
        question = Question(
            question=body.get("question"),
            answer=body.get("answer"),
            category=int(body.get("category")),
            difficulty=int(body.get("difficulty"))
        )
        # save question to the db
        question.insert()
        return jsonify({
            "question": question.format,
            "message": "Question successfully created."
        }), 201

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        """
            Handles search requests for questions.
            returns:
            - a list of paginated questions
            - total number of questions
            - current category
            - categories
        """
        pass

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app
