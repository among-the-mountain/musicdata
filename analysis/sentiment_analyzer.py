"""
Sentiment analysis module using Qwen3-30B-A3B API
"""
import requests
import json
from typing import List, Dict


class SentimentAnalyzer:
    """Analyze sentiment of music comments using Qwen3-30B-A3B"""
    
    def __init__(self, api_key: str = None):
        self.url = "https://api.modelarts-maas.com/v1/chat/completions"
        self.api_key = api_key or "MAAS_API_KEY"  # Should be replaced with actual key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def analyze_comment_batch(self, comments: List[str], batch_size: int = 10) -> Dict:
        """Analyze sentiment of a batch of comments"""
        if not comments:
            return {'positive': 0, 'neutral': 0, 'negative': 0, 'trend': []}
        
        # For demo purposes, we'll use a simple rule-based approach
        # In production with valid API key, use the Qwen API
        return self._analyze_simple(comments)
    
    def _analyze_simple(self, comments: List[str]) -> Dict:
        """Simple rule-based sentiment analysis (fallback)"""
        positive_keywords = ['好', '棒', '喜欢', '爱', '赞', '美', '优秀', '精彩', '完美', '感动', '温柔', '治愈']
        negative_keywords = ['差', '烂', '讨厌', '恨', '垃圾', '难听', '失望', '糟糕', '无聊', '伤心']
        
        sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        for comment in comments:
            pos_count = sum(1 for word in positive_keywords if word in comment)
            neg_count = sum(1 for word in negative_keywords if word in comment)
            
            if pos_count > neg_count:
                sentiments['positive'] += 1
            elif neg_count > pos_count:
                sentiments['negative'] += 1
            else:
                sentiments['neutral'] += 1
        
        total = len(comments)
        return {
            'positive': sentiments['positive'],
            'neutral': sentiments['neutral'],
            'negative': sentiments['negative'],
            'positive_pct': round(sentiments['positive'] / total * 100, 2) if total > 0 else 0,
            'neutral_pct': round(sentiments['neutral'] / total * 100, 2) if total > 0 else 0,
            'negative_pct': round(sentiments['negative'] / total * 100, 2) if total > 0 else 0,
        }
    
    def analyze_with_api(self, comments: List[str]) -> Dict:
        """Analyze using Qwen3-30B-A3B API (requires valid API key)"""
        # Prepare batch of comments
        comment_text = '\n'.join(comments[:50])  # Limit to 50 comments
        
        prompt = f"""请分析以下音乐评论的情感倾向，统计正面、中性、负面评论的数量。
评论内容：
{comment_text}

请返回JSON格式：
{{"positive": 数量, "neutral": 数量, "negative": 数量}}
"""
        
        data = {
            "model": "qwen3-30b-a3b",
            "messages": [
                {"role": "system", "content": "你是一个专业的情感分析助手。"},
                {"role": "user", "content": prompt}
            ],
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
        
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                data=json.dumps(data),
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Parse the response to extract sentiment counts
                # This is simplified - actual parsing depends on API response format
                return self._parse_api_response(result)
            else:
                print(f"API request failed: {response.status_code}")
                return self._analyze_simple(comments)
        except Exception as e:
            print(f"Error calling API: {e}")
            return self._analyze_simple(comments)
    
    def _parse_api_response(self, response: Dict) -> Dict:
        """Parse API response to extract sentiment data"""
        # This is a placeholder - actual implementation depends on API response format
        try:
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '{}')
            sentiment_data = json.loads(content)
            return sentiment_data
        except:
            return {'positive': 0, 'neutral': 0, 'negative': 0}
    
    def generate_sentiment_summary(self, comments: List[str]) -> str:
        """Generate a summary of sentiment analysis"""
        analysis = self.analyze_comment_batch(comments)
        
        total = analysis['positive'] + analysis['neutral'] + analysis['negative']
        if total == 0:
            return "暂无评论数据"
        
        summary = f"""
评论情感分析总结：
- 总评论数：{total}
- 正面评论：{analysis['positive']} ({analysis.get('positive_pct', 0)}%)
- 中性评论：{analysis['neutral']} ({analysis.get('neutral_pct', 0)}%)
- 负面评论：{analysis['negative']} ({analysis.get('negative_pct', 0)}%)

整体情感倾向：{'正面' if analysis['positive'] > analysis['negative'] else '负面' if analysis['negative'] > analysis['positive'] else '中性'}
"""
        return summary


if __name__ == "__main__":
    # Test sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    test_comments = [
        "这首歌太好听了！",
        "一般般吧",
        "很喜欢这种风格",
        "不太喜欢",
        "超级棒的音乐"
    ]
    
    result = analyzer.analyze_comment_batch(test_comments)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(analyzer.generate_sentiment_summary(test_comments))
