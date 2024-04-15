from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    user_input = request.form['user_input']
    return redirect(url_for('wrapped', user_id=user_input))
  
  context = {
      "top_songs_week": ["Song1", "Song2", "Song3", "Song4", "Song5"],
      "top_songs_month": ["So1", "Song2", "Song3", "Song4", "Song5"],
      "top_artists_week": ["Artist1", "Artist2", "Artist3", "Artist4", "Artist5"],
      "top_artists_month": ["Artist1", "Artist2", "Artist3", "Artist4", "Artist5"],
  }

  return render_template('index.html', **context)


@app.route('/wrapped/<user_id>')
def wrapped(user_id):
    context = {
       "user_id": user_id,
       "personality_type": "The Voyager",
       "personality_traits": ["Exploration", "Newness", "Loyalty", "Commonality"]
    }    

    return render_template('wrapped.html', **context)

app.run(debug=True)