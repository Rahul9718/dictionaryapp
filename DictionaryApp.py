from flask import Flask , jsonify , request, abort, make_response
# HTTPBasicAuth securtiy ke liye hota h isme flask apne ap password match karta h ki user ne sahi password dala h ya ni
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
import operator

app = Flask(__name__)
# is wali line se code apne ap update hota rahega hame python se bar bar code run ni karna padega
app.config.update({
    "DEBUG": True
})

users = [
    { 'name': 'rahul',
      'password': 'a'
    },
    { 'name': 'shivam',
      'password': 'b'
    }
]

words = [
    { 'word': 'happy',
      'note': 'happy ka matlb hota h khushi ya khush',
      'difficulty': 5,
          'name': 'rahul',
      'id': 1
    },
    {'word': 'sad',
     'note': 'happy ka matlb hota h khushi ya khush',
     'difficulty': 3,
     'name': 'rahul',
     'id': 3
    },
    {'word': 'apple',
     'note': 'happy ka matlb hota h khushi ya khush',
     'difficulty': 9,
     'name': 'rahul',
     'id': 2
    }
    ]

@auth.get_password
def get_password(username):
    # ye comprihension list h jisse hum for loop chalte h or condition dalte h
    new_user = [user for user in users if username == user['name']]

    if len(new_user) == 0:
        abort(404)
    return new_user[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'unauthorized access'}),401)

@app.route('/get_words', methods=['GET'])
@auth.login_required
def get_words():
    # auth.username current username ki value store karta h
    new_words = [word for word in words if auth.username() == word['name']]
    # url me jo question mark ke bad hota h ye use trigger karta hai or fir uski value hume ? dal kar hume code me change kar sakte h
    input = request.args.get('input')
    if input == 'id':
        # dictionary ko sort karne ke liye is line ka use kiya hai
        new_words = sorted(new_words, key=lambda  k : k['id'])
    elif input == 'word':
        new_words = sorted(new_words, key=lambda k: k['word'])
    elif input == 'difficulty':
        new_words = sorted(new_words, key=lambda k: k['difficulty'])
    else:
        abort(400)
    return jsonify({'users':new_words})

@app.route('/post_user', methods = ['POST'])
def add_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    add = {
        'name': request.json['name'],
        'password' : request.json['password']
    }
    users.append(add)
    return jsonify({"user": add}), 201

@app.route('/post_words', methods = ['POST'])
def add_word():
    if not request.json or not 'word' in request.json:
        abort(400)
    add_more_word = {
        # words wali dicnary ke last item ki id me 5 plus kar de
        'id' : words[-1]['id'] + 1,
        'name' : auth.username(),
        'word': request.json['word'],
        'note': request.json['note'],
        'difficulty': request.json['difficulty']
    }
    words.append(add_more_word)
    return jsonify({"words": add_more_word}), 201

if __name__ == '__main__':
    app.run()