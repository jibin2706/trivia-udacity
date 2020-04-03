import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    result = []
    for category in categories:
      result.append(category.format())

    return jsonify({
      'success': True,
      'data': result,
      'total': len(categories)
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, int)
    questions = Question.query.all()

    paginate_questions = paginate_data(questions, page)
    result = []
    for question in questions:
      result.append(question.format())

    return jsonify({
      'success': True,
      'data': result,
      'total': len(questions)
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/question/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)
    print(question)
    if question is None:
      return abort(400)

    try:
      question.delete()
    except:
      return abort(400)

    return jsonify({
      'success': True,
      'question_id': question_id
    })



  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/question', methods=['POST'])
  def add_question():
    data = request.get_json()

    try:
      question = Question(question=data['question'], answer=data['answer'], category=data['category'], difficulty=data['difficulty'])
      question.insert()
    except:
      return abort(400)
    
    return jsonify({
      'success': True
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/<search_term>', methods=['POST'])
  def search_questions(search_term):
    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    result = [question.format() for question in questions]
    
    return jsonify({
      'success': True,
      'data': result,
      'total': len(result)
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/category/<category_type>')
  def get_question_from_category(category_type):
    questions = Question.query.join(Category, Question.category == Category.id).filter(Category.type == category_type.capitalize()).all()
    result = [question.format() for question in questions]

    return jsonify({
      'success': True,
      'data': result,
      'total': len(questions)
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
  @app.route('/quiz/question', methods=['POST'])
  def next_question():
    data = request.get_json()
    question = Question.query.join(Category, Question.category == Category.id)\
      .filter(and_(Category.id == data['category'], Question.id != data['previous_question_id']))\
      .order_by(func.random())\
      .first()
    
    if question is None:
      return abort(422)

    return jsonify({
      'success': True,
      'data': question.format()
    })


  # Error handlers
  @app.errorhandler(400)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'data': 'Bad Request'
    })

  @app.errorhandler(404)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'data': 'Page not found'
    })
  
  @app.errorhandler(405)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'data': 'Method not allowed'
    })
  
  @app.errorhandler(422)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'data': 'Request cannot be processed'
    })


  # Utility functions
  def paginate_data(list, page = 1, items=10):
    """
    Pagiantes data

    Parameters
    ----------
    list : list
      Model objects in a Python list
    page : int
      Which page you want to return
    items: int
      Number of items in a page

    Returns
    -------
    list
      Model objects in a Python list

    """
    start = (page - 1) * items
    end = start + items

    return list[start:end]

  return app