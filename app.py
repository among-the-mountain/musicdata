"""
Flask Application for Music Data Analysis and Visualization
"""
from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis.data_analyzer import MusicDataAnalyzer
from analysis.sentiment_analyzer import SentimentAnalyzer

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


# Initialize analyzers
data_file = os.path.join(os.path.dirname(__file__), 'data', 'music_data.json')
analyzer = MusicDataAnalyzer(data_file)
sentiment_analyzer = SentimentAnalyzer()


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/overview')
def api_overview():
    """Get data overview"""
    overview = analyzer.get_data_overview()
    return jsonify(overview)


@app.route('/api/album-types')
def api_album_types():
    """Get album types analysis"""
    data = analyzer.analyze_album_types()
    return jsonify(data)


@app.route('/api/release-trend')
def api_release_trend():
    """Get release trend analysis"""
    data = analyzer.analyze_release_trend()
    return jsonify(data)


@app.route('/api/music-genres')
def api_music_genres():
    """Get music genres analysis"""
    data = analyzer.analyze_music_genres()
    return jsonify(data)


@app.route('/api/top-album-types')
def api_top_album_types():
    """Get top 10 album types"""
    data = analyzer.analyze_top_album_types(top_n=10)
    return jsonify(data)


@app.route('/api/top-artists')
def api_top_artists():
    """Get top 5 artists"""
    data = analyzer.analyze_top_artists(top_n=5)
    return jsonify(data)


@app.route('/api/wordcloud')
def api_wordcloud():
    """Get word cloud data"""
    data = analyzer.generate_wordcloud_data()
    return jsonify(data)


@app.route('/api/sentiment')
def api_sentiment():
    """Get sentiment analysis of comments"""
    comments = analyzer.get_comments_for_sentiment()
    sentiment_data = sentiment_analyzer.analyze_comment_batch(comments)
    return jsonify(sentiment_data)


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)


if __name__ == '__main__':
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Warning: Data file {data_file} not found!")
        print("Please run crawler/netease_crawler.py first to collect data.")
        # Create empty data file
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump({'songs': [], 'comments': []}, f)
    
    print("Starting Flask application...")
    print("Visit http://localhost:5000 to view the dashboard")
    app.run(debug=True, host='0.0.0.0', port=5000)
