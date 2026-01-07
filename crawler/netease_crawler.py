"""
NetEase Cloud Music Crawler
Based on https://github.com/LindiaC/music163-miningr
"""
import requests
import json
import time
import random
from typing import List, Dict
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii


class NetEaseMusicCrawler:
    """NetEase Cloud Music data crawler with anti-crawling handling"""
    
    def __init__(self):
        self.base_url = "https://music.163.com"
        self.api_url = "https://music.163.com/weapi"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://music.163.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.session = requests.Session()
        
    def _get_params_encSecKey(self, data: dict) -> dict:
        """Generate encrypted params for API request"""
        # This is a simplified version - NetEase's encryption is complex
        # For production, you'd need to implement full encryption
        return {
            'params': self._encrypt(json.dumps(data)),
            'encSecKey': self._get_encSecKey()
        }
    
    def _encrypt(self, text: str) -> str:
        """Encrypt data (simplified)"""
        # Note: This is a placeholder. Real implementation needs AES encryption
        # matching NetEase's algorithm
        return base64.b64encode(text.encode()).decode()
    
    def _get_encSecKey(self) -> str:
        """Get encrypted security key (simplified)"""
        return "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca853ae8f65e6f6f8b7e5a47e7d8a9d4e1c1cfe44fc8e3a20a0d29e4c1b"
    
    def get_playlist_detail(self, playlist_id: str) -> Dict:
        """Get playlist detail including songs"""
        url = f"{self.base_url}/api/playlist/detail"
        params = {'id': playlist_id}
        
        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Failed to get playlist {playlist_id}: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Error getting playlist {playlist_id}: {e}")
            return {}
    
    def get_hot_playlists(self, limit: int = 50) -> List[Dict]:
        """Get hot playlists"""
        url = f"{self.base_url}/api/playlist/hot"
        params = {'limit': limit}
        
        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('playlists', [])
            else:
                print(f"Failed to get hot playlists: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting hot playlists: {e}")
            return []
    
    def get_song_detail(self, song_id: str) -> Dict:
        """Get song detail"""
        url = f"{self.base_url}/api/song/detail"
        params = {'id': song_id, 'ids': f'[{song_id}]'}
        
        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('songs', [{}])[0] if data.get('songs') else {}
            else:
                return {}
        except Exception as e:
            print(f"Error getting song {song_id}: {e}")
            return {}
    
    def get_song_comments(self, song_id: str, limit: int = 100, offset: int = 0) -> Dict:
        """Get song comments"""
        url = f"{self.base_url}/api/v1/resource/comments/R_SO_4_{song_id}"
        params = {
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Failed to get comments for song {song_id}: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Error getting comments for song {song_id}: {e}")
            return {}
    
    def crawl_music_data(self, num_playlists: int = 10, songs_per_playlist: int = 20) -> Dict:
        """
        Crawl music data from NetEase Cloud Music
        Returns a dictionary with songs, albums, artists, and comments
        """
        all_songs = []
        all_comments = []
        
        print("Fetching hot playlists...")
        playlists = self.get_hot_playlists(limit=num_playlists)
        
        for idx, playlist in enumerate(playlists[:num_playlists], 1):
            print(f"Processing playlist {idx}/{num_playlists}: {playlist.get('name', 'Unknown')}")
            
            playlist_id = playlist.get('id')
            if not playlist_id:
                continue
            
            # Get playlist detail
            detail = self.get_playlist_detail(str(playlist_id))
            tracks = detail.get('result', {}).get('tracks', [])[:songs_per_playlist]
            
            for track in tracks:
                song_info = {
                    'id': track.get('id'),
                    'name': track.get('name'),
                    'artists': [artist.get('name') for artist in track.get('artists', [])],
                    'album': track.get('album', {}).get('name'),
                    'album_type': track.get('album', {}).get('type', 'Unknown'),
                    'publish_time': track.get('album', {}).get('publishTime', 0),
                    'duration': track.get('duration', 0),
                    'popularity': track.get('popularity', 0)
                }
                all_songs.append(song_info)
                
                # Get some comments for sentiment analysis (first 5 songs from each playlist)
                if len([s for s in all_songs if s['id'] == song_info['id']]) == 1 and len(all_songs) % 5 == 0:
                    time.sleep(random.uniform(0.5, 1.5))  # Rate limiting
                    comments_data = self.get_song_comments(str(song_info['id']), limit=20)
                    comments = comments_data.get('comments', [])
                    
                    for comment in comments:
                        all_comments.append({
                            'song_id': song_info['id'],
                            'song_name': song_info['name'],
                            'content': comment.get('content', ''),
                            'time': comment.get('time', 0),
                            'liked_count': comment.get('likedCount', 0)
                        })
            
            # Rate limiting between playlists
            time.sleep(random.uniform(1, 2))
        
        return {
            'songs': all_songs,
            'comments': all_comments,
            'crawl_time': time.time()
        }


def save_crawled_data(data: Dict, filename: str = 'data/music_data.json'):
    """Save crawled data to JSON file"""
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {filename}")


def load_crawled_data(filename: str = 'data/music_data.json') -> Dict:
    """Load crawled data from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found")
        return {}


if __name__ == "__main__":
    # Test crawler
    crawler = NetEaseMusicCrawler()
    print("Starting to crawl music data...")
    data = crawler.crawl_music_data(num_playlists=5, songs_per_playlist=10)
    
    print(f"\nCrawled {len(data['songs'])} songs")
    print(f"Crawled {len(data['comments'])} comments")
    
    save_crawled_data(data)
