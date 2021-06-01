import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, query):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in query]
    selected_questions = formatted_questions[start:end]

    return selected_questions


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    '''
    CORS(app, resources={r"*": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,'
                             'DELETE,OPTIONS')
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories_query = Category.query.all()
        items = {}
        for category in categories_query:
            items[category.id] = category.type
        result = {
                  "success": True,
                  "categories": items
                }
        return jsonify(result)
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at
    the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():

        questions_query = Question.query.order_by(Question.id).all()

        paginated_questions = paginate_questions(request, questions_query)
        if not paginated_questions:
            abort(404)
        categories_query = Category.query.all()
        if not categories_query:
            abort(404)

        items = {}
        for category in categories_query:
            items[category.id] = category.type

        result = jsonify({
          'success': True,
          'questions': paginated_questions,
          'total_questions': len(questions_query),
          'categories': items,
          'currentCategory': None,
        })
        return result

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
     the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)
        if not question:
            abort(404)
        question.delete()
        return jsonify({
          'success': True,
          'id': question.id
        })
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and
    the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            body = request.get_json()
            if (('question' not in body) or ('answer' not in body) or
                    ('difficulty' not in body) or ('category' not in body)):
                abort(400)
            if (not body['question']) or (not body['answer']):
                abort(400)
            question = Question(question=body['question'],
                                answer=body['answer'],
                                difficulty=body['difficulty'],
                                category=body['category'])
            question.insert()
            return jsonify({
                'success': True,
                'message': "question added"
              })
        except Exception:
            abort(400)
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search():
        try:
            body = request.get_json()

            search = Question.query.filter(
              Question.question.ilike(f"%{body['searchTerm']}%")).all()
            paginated_questions = paginate_questions(request, search)
            return jsonify({
              'success': True,
              'questions': paginated_questions,
              'total_questions': len(search),
            })
        except Exception:
            abort(400)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:id>/questions')
    def get_categorized_questions(id):

        questions = Question.query.filter_by(category=id).all()
        if not questions:
            abort(404)

        paginated_questions = paginate_questions(request, questions)

        return jsonify({
          'success': True,
          'questions': paginated_questions,
          'total_questions': len(questions),
          'current_category': id
        })

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
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            data = request.get_json()
            id = int(data['quiz_category']['id'])
            questions = []
            if id != 0:
                questions = Question.query.filter(
                  Question.category == id).all()
            else:
                questions = Question.query.all()

            if not questions:
                abort(404)

            while True:
                question = random.choice(questions)
                if question.id not in data['previous_questions']:
                    question = question.format()
                    break
                if len(questions) == len(data['previous_questions']):
                    question = False
                    break

            return jsonify({
              'success': True,
              'question': question
            })
        except Exception:
            abort(400)

    # # '''
    # # @TODO:
    # # Create error handlers for all expected errors
    # # including 404 and 422.
    # # '''
    @app.errorhandler(404)
    def handle404(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found",
        }), 404

    @app.errorhandler(400)
    def handle400(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request",
        }), 400

    @app.errorhandler(422)
    def handle422(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unproccessable",
        }), 422

    @app.errorhandler(500)
    def handle500(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error",
        }), 500

    @app.errorhandler(405)
    def handle405(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed",
        }), 405

    return app
