import os
from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from helpers import format_paginated_questions

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Allow '*' for origins.
    CORS(app, resources={r"/*": {"origins": "*"}})

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

    @app.route("/questions")
    def get_questions():
        """
            Handles GET requests for questions categories,
            including pagination.
            returns:
            - a list of paginated questions
            - total number of questions
            - next url
            - prev url
        """
        page = request.args.get('page', 1, type=int)
        questions = Question.query.join(
            Category, Category.id == Question.category).add_columns(
            Category.type).paginate(page, QUESTIONS_PER_PAGE, False)

        # Return serializable paginated questions.
        paginated_results = format_paginated_questions(questions.items)

        # Next page navigation.
        next_url = url_for("get_questions", page=questions.next_num) \
            if questions.has_next else None

        # Previous page navigation.
        prev_url = url_for("get_questions", page=questions.prev_num) \
            if questions.has_prev else None

        # Query total number of questions.
        total_questions = len(Question.query.all())

        return jsonify({
            "questions": paginated_results,
            "next_url": next_url,
            "prev_url": prev_url,
            "total_questions": total_questions
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
            "question": question.format(),
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
        search_term = request.get_json()["search_term"]
        page = request.args.get('page', 1, type=int)

        questions = Question.query.filter(func.lower(
            Question.question).contains(func.lower(search_term))).join(
            Category, Category.id == Question.category).add_columns(
            Category.type).paginate(page, QUESTIONS_PER_PAGE, False)

        # Return serializable paginated search results.
        search_results = format_paginated_questions(questions.items)

        # Next page navigation.
        next_url = url_for("get_questions", page=questions.next_num) \
            if questions.has_next else None

        # Previous page navigation.
        prev_url = url_for("get_questions", page=questions.prev_num) \
            if questions.has_prev else None

        total_search_results = len(search_results)

        return jsonify({
            "questions": search_results,
            "next_url": next_url,
            "prev_url": prev_url,
            "total_search_results": total_search_results
        }), 201

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        """
            Handles GET requests for questions based on category.
            returns:
            - a list of paginated questions
            - total number of questions
            - current category
        """
        page = request.args.get('page', 1, type=int)
        questions = Question.query.filter_by(category=category_id).join(
            Category, Category.id == Question.category).add_columns(
            Category.type).all()
        paginated_results = pagination(page, questions)
        return jsonify({
            "questions": paginated_results,
            "total_questions": len(paginated_results)
        }), 200

    @app.route("/quiz", methods=["POST"])
    def get_quiz_questions():
        """
            Handles POST requests for quizzes.
            returns:
            - random question
        """
        pass

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
