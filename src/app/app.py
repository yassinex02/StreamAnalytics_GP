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
    personality_type = "LALALA"
    personality_image = "../static/images/ENLC.png"

    return render_template('wrapped.html', user_id=user_id, personality_type=personality_type, personality_image=personality_image)

app.run(debug=True)