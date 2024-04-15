from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    user_input = request.form['user_input']
    return redirect(url_for('wrapped', user_id=user_input))

  return render_template('index.html')


@app.route('/wrapped/<user_id>')
def wrapped(user_id):
    context = {
       "user_id": user_id,
       "personality_type": "The Voyager",
       "first_trait": "Exploration",
       "second_trait": "Newness",
       "third_trait": "Loyalty",
       "fourth_trait": "Commonality",
    }    

    return render_template('wrapped.html', **context)

app.run(debug=True)