"""
Data analysis module for music data
Provides various analysis functions for the visualization
"""
import json
import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime
from typing import Dict, List
import jieba


class MusicDataAnalyzer:
    """Analyze music data for visualization"""
    
    def __init__(self, data_file: str = 'data/music_data.json'):
        self.data_file = data_file
        self.data = self._load_data()
        self.df_songs = self._create_songs_dataframe()
        self.df_comments = self._create_comments_dataframe()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Data file {self.data_file} not found")
            return {'songs': [], 'comments': []}
    
    def _create_songs_dataframe(self) -> pd.DataFrame:
        """Create DataFrame from songs data"""
        songs = self.data.get('songs', [])
        if not songs:
            return pd.DataFrame()
        
        df = pd.DataFrame(songs)
        
        # Convert publish_time to datetime
        if 'publish_time' in df.columns:
            df['publish_date'] = pd.to_datetime(df['publish_time'], unit='ms', errors='coerce')
            df['publish_year'] = df['publish_date'].dt.year
            df['publish_month'] = df['publish_date'].dt.month
        
        # Flatten artists list
        if 'artists' in df.columns:
            df['artist_name'] = df['artists'].apply(lambda x: ', '.join(x) if x else 'Unknown')
            df['primary_artist'] = df['artists'].apply(lambda x: x[0] if x and len(x) > 0 else 'Unknown')
        
        return df
    
    def _create_comments_dataframe(self) -> pd.DataFrame:
        """Create DataFrame from comments data"""
        comments = self.data.get('comments', [])
        if not comments:
            return pd.DataFrame()
        
        df = pd.DataFrame(comments)
        
        # Convert time to datetime
        if 'time' in df.columns:
            df['comment_date'] = pd.to_datetime(df['time'], unit='ms', errors='coerce')
        
        return df
    
    def get_data_overview(self) -> Dict:
        """Get overview statistics"""
        return {
            'total_songs': len(self.df_songs),
            'total_artists': self.df_songs['primary_artist'].nunique() if not self.df_songs.empty else 0,
            'total_albums': self.df_songs['album'].nunique() if not self.df_songs.empty else 0,
            'total_comments': len(self.df_comments),
            'date_range': {
                'start': str(self.df_songs['publish_date'].min()) if not self.df_songs.empty else 'N/A',
                'end': str(self.df_songs['publish_date'].max()) if not self.df_songs.empty else 'N/A'
            }
        }
    
    def analyze_album_types(self) -> Dict:
        """Analyze different album types distribution"""
        if self.df_songs.empty or 'album_type' not in self.df_songs.columns:
            return {'labels': [], 'data': [], 'popularity': {}}
        
        # Count by album type
        type_counts = self.df_songs['album_type'].value_counts().to_dict()
        
        # Average popularity by album type
        type_popularity = self.df_songs.groupby('album_type')['popularity'].mean().to_dict()
        
        return {
            'labels': list(type_counts.keys()),
            'data': list(type_counts.values()),
            'popularity': type_popularity
        }
    
    def analyze_release_trend(self) -> Dict:
        """Analyze music release trend over time"""
        if self.df_songs.empty or 'publish_year' not in self.df_songs.columns:
            return {'years': [], 'counts': []}
        
        # Filter out invalid years
        df_valid = self.df_songs[self.df_songs['publish_year'].notna()]
        df_valid = df_valid[df_valid['publish_year'] > 1900]
        df_valid = df_valid[df_valid['publish_year'] <= datetime.now().year]
        
        # Count by year
        year_counts = df_valid['publish_year'].value_counts().sort_index()
        
        return {
            'years': [int(year) for year in year_counts.index],
            'counts': year_counts.values.tolist()
        }
    
    def analyze_music_genres(self) -> Dict:
        """Analyze music genre distribution"""
        # Note: NetEase API doesn't always provide genre info
        # We'll use album_type as a proxy or implement genre detection
        if self.df_songs.empty:
            return {'labels': [], 'data': []}
        
        # For demo purposes, we'll use album names to infer genres
        # In production, you'd use proper genre classification
        genre_keywords = {
            '流行': ['流行', 'Pop', 'popular'],
            '摇滚': ['摇滚', 'Rock', 'rock'],
            '古典': ['古典', 'Classical', 'classic'],
            '民谣': ['民谣', 'Folk', 'folk'],
            '电子': ['电子', 'Electronic', 'EDM'],
            '说唱': ['说唱', 'Rap', 'Hip-Hop', 'hip-hop'],
            '爵士': ['爵士', 'Jazz', 'jazz'],
            '其他': []
        }
        
        def classify_genre(name, album):
            text = f"{name} {album}".lower()
            for genre, keywords in genre_keywords.items():
                if genre == '其他':
                    continue
                for keyword in keywords:
                    if keyword.lower() in text:
                        return genre
            return '其他'
        
        if 'name' in self.df_songs.columns and 'album' in self.df_songs.columns:
            self.df_songs['genre'] = self.df_songs.apply(
                lambda x: classify_genre(str(x['name']), str(x['album'])), axis=1
            )
            genre_counts = self.df_songs['genre'].value_counts().to_dict()
        else:
            genre_counts = {'其他': len(self.df_songs)}
        
        return {
            'labels': list(genre_counts.keys()),
            'data': list(genre_counts.values())
        }
    
    def analyze_top_album_types(self, top_n: int = 10) -> Dict:
        """Analyze top N album types"""
        if self.df_songs.empty or 'album_type' not in self.df_songs.columns:
            return {'labels': [], 'data': []}
        
        top_types = self.df_songs['album_type'].value_counts().head(top_n)
        
        return {
            'labels': top_types.index.tolist(),
            'data': top_types.values.tolist()
        }
    
    def analyze_top_artists(self, top_n: int = 5) -> Dict:
        """Analyze top N artists by number of works"""
        if self.df_songs.empty or 'primary_artist' not in self.df_songs.columns:
            return {'labels': [], 'data': []}
        
        top_artists = self.df_songs['primary_artist'].value_counts().head(top_n)
        
        return {
            'labels': top_artists.index.tolist(),
            'data': top_artists.values.tolist()
        }
    
    def generate_wordcloud_data(self) -> Dict:
        """Generate word cloud data from song names"""
        if self.df_songs.empty or 'name' not in self.df_songs.columns:
            return {'words': []}
        
        # Combine all song names
        all_names = ' '.join(self.df_songs['name'].astype(str).tolist())
        
        # Use jieba for Chinese word segmentation
        words = jieba.cut(all_names)
        
        # Filter out common stop words and single characters
        stop_words = {'的', '了', '和', '是', '就', '都', '而', '及', '与', '着', '之', '在', '有', '一', '不', '我', '你', '他'}
        word_list = [word for word in words if len(word) > 1 and word not in stop_words]
        
        # Count word frequencies
        word_freq = Counter(word_list)
        
        # Get top 100 words
        top_words = word_freq.most_common(100)
        
        return {
            'words': [{'text': word, 'value': count} for word, count in top_words]
        }
    
    def get_comments_for_sentiment(self) -> List[str]:
        """Get comment texts for sentiment analysis"""
        if self.df_comments.empty or 'content' not in self.df_comments.columns:
            return []
        
        return self.df_comments['content'].tolist()


if __name__ == "__main__":
    # Test analyzer
    analyzer = MusicDataAnalyzer()
    
    print("Data Overview:", json.dumps(analyzer.get_data_overview(), indent=2, ensure_ascii=False))
    print("\nAlbum Types:", json.dumps(analyzer.analyze_album_types(), indent=2, ensure_ascii=False))
    print("\nTop Artists:", json.dumps(analyzer.analyze_top_artists(), indent=2, ensure_ascii=False))
