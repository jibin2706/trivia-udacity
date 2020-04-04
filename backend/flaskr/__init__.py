import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
from sqlalchemy.sql.operators import ColumnOperators
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"*": {"origins": "*"}})


  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
    return response

  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    result = [category.format() for category in categories]

    return jsonify({
      'success': True,
      'data': result,
      'total': len(categories)
    })

  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, int)
    questions = Question.query.all()
    categories = Category.query.all()

    paginate_questions = paginate_data(questions, page)
    question_result = [question.format() for question in paginate_questions]
    categories_result = [category.format() for category in categories]

    if question_result == []:
      return abort(400)

    return jsonify({
      'success': True,
      'data': {
        'questions': question_result,
        'categories': categories_result
      },
      'total': len(questions),
      'category': 'All'
    })
 
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
    }), 200

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

  @app.route('/questions', methods=['POST'])
  def search_questions():
    data = request.get_json()
    search_term = data.get('search_term')

    if 'search_term' in data:
      questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      result = [question.format() for question in questions]
    else:
      return abort(400)
    
    return jsonify({
      'success': True,
      'data': result,
      'total': len(result)
    })

  @app.route('/category/<int:category_id>/questions')
  def get_question_from_category(category_id):
    questions = Question.query.join(Category, Question.category == Category.id).filter(Category.id == category_id).all()
    result = [question.format() for question in questions]

    return jsonify({
      'success': True,
      'data': result,
      'total': len(questions),
      'category': category_id
    })

  @app.route('/quiz/question', methods=['POST'])
  def next_question():
    data = request.get_json()
    if data['category'] == 0:
      question = Question.query.join(Category, Question.category == Category.id)\
      .filter(ColumnOperators.notin_(Question.id, data['previous_questions']))\
      .order_by(func.random())\
      .first()
    else:  
      question = Question.query.join(Category, Question.category == Category.id)\
      .filter(and_(Category.id == data['category'], ColumnOperators.notin_(Question.id, data['previous_questions'])))\
      .order_by(func.random())\
      .first()
    
    if question is None:
      return abort(400)

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
    }), 400

  @app.errorhandler(404)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'data': 'Page not found'
    }), 404
  
  @app.errorhandler(405)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'data': 'Method not allowed'
    }), 405
  
  @app.errorhandler(422)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'data': 'Request cannot be processed'
    }), 422


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