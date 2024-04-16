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
       "personality_traits": ["Exploration", "Newness", "Loyalty", "Commonality"],
       "total_listens_week": 400,
       "total_listening_time_week": 40,
       "total_listens_month": 400,
       "total_listening_time_month": 40,
       "top_song_week": "FEARLESS",
       "percentile_week": "Top 1%",
       "top_song_month": "You are my Sunshine",
       "percentile_month": "Top 1%",
       "top_5_week": ["Song1", "Song2", "Song3", "Song4", "Song5"],
       "top_5_month": ["Track1", "Track2", "Track3", "Track4", "Track5"]
    }    

    return render_template('wrapped.html', **context)

app.run(debug=True)