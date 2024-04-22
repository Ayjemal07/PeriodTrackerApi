from flask import Blueprint, request, jsonify, render_template
from app.helpers import token_required
from app.models import db, User, Cycle, cycle_schema, cycles_schema
from werkzeug.security import check_password_hash



#this line of code is preparing a blueprint named api 
#that will group all API-related routes under the /api. F.example: /api/users

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/cycle', methods = ['POST'])
@token_required
def create_cycle(current_user):
    last_period_date = request.json['last_period_date']

    # if current_user.default_duration:
    #     period_duration=current_user.default_duration
    # else:
    #     period_duration  = request.json['period_duration']
    # user_token = current_user.token
    period_duration  = request.json['period_duration']

    print(f'BIG TESTER: {current_user.token}')

    cycle = Cycle(last_period_date ,period_duration, user_token = user_token )
    db.session.add(cycle)
    db.session.commit()
    response = cycle_schema.dump(cycle)
    return jsonify(response)


@api.route('/cycles', methods = ['GET'])
@token_required
def get_cycles(current_user_token):
    a_user = current_user_token.token
    cycles= Cycle.query.filter_by(user_token = a_user).all()
    response = cycles_schema.dump(cycles)
    return jsonify(response)

@api.route('/cycles/<id>', methods=['GET'])
@token_required
def get_single_cycle(current_user_token, id):
    user_token = current_user_token.token
    cycle = Cycle.query.filter_by(id=id, user_token=user_token).first()
    if cycle:
        response = cycle_schema.dump(cycle)
        return jsonify(response)
    else:
        return jsonify({"message": "Cycle not found"}), 404


@api.route('/cycles/<id>', methods = ['POST','PUT'])
@token_required
def update_cycle(current_user_token,id):
    cycle = Cycle.query.get(id) 
    cycle.last_period_date = request.json['last_period_date']
    cycle.period_duration = request.json['period_duration']
    cycle.user_token = current_user_token.token

    db.session.commit()
    response = cycle_schema.dump(cycle)
    return jsonify(response)

@api.route('/cycles/<id>', methods = ['DELETE'])
@token_required
def delete_cycle(current_user_token, id):
    cycle = Cycle.query.get(id)
    if cycle.user_token!=current_user_token.token:
        return {"error":"This cycle does not belong to you"}
    db.session.delete(cycle)
    db.session.commit()
    response = cycle_schema.dump(cycle)
    return jsonify(response)


@api.route('/login', methods = ['POST'])
def get_token():
    data=request.json
    email=data['email']
    password=data['password']

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, password):
        return jsonify({'token': logged_user.token}), 200
    
    else:
        return jsonify({'error': 'Invalid email or password'}), 401
    

