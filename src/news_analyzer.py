import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAnalyzer:
    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.featherless_api_key = os.getenv("FEATHERLESS_API_KEY")
        self.featherless_base_url = os.getenv("FEATHERLESS_API_BASE", "https://api.featherless.ai/v1")

    def fetch_headlines(self, query="finance banking economy"):
        """
        Fetches latest headlines from NewsAPI.
        """
        if not self.news_api_key:
            logger.warning("NEWS_API_KEY not found in .env. Using mock headlines.")
            return [
                "JPM stock drops 50% due to a 2-for-1 split.",
                "Lehman Brothers reports $3B loss in subprime.",
                "Global markets rally on positive employment data.",
                "Central Bank raises interest rates by 25 basis points."
            ]

        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={self.news_api_key}&language=en"
        try:
            response = requests.get(url)
            data = response.json()
            if data['status'] == 'ok':
                return [article['title'] for article in data['articles'][:10]]
            else:
                logger.error(f"NewsAPI error: {data.get('message')}")
                return []
        except Exception as e:
            logger.error(f"Failed to fetch headlines: {e}")
            return []

    def get_fallback_analysis(self, headline):
        """
        Keyword-based sentiment analysis as a fallback for AI.
        """
        systemic_keywords = ['collapse', 'crisis', 'loss', 'subprime', 'default', 'warning', 'bankrupt', 'contagion', 'crash']
        headline_lower = headline.lower()
        
        if any(word in headline_lower for word in systemic_keywords):
            return {
                "classification": "Systemic Warning",
                "reasoning": "Fallback: Detected high-risk keywords in headline.",
                "health_score": 2
            }
        
        # Check for stock splits or neutral events
        if 'split' in headline_lower or 'dividend' in headline_lower:
            return {
                "classification": "Idiosyncratic/Neutral",
                "reasoning": "Fallback: Detected neutral corporate action (split/dividend).",
                "health_score": 8
            }
            
        return {
            "classification": "Neutral",
            "reasoning": "Fallback: Headline appears non-critical.",
            "health_score": 6
        }

    def analyze_risk(self, headline):
        """
        Uses Featherless AI (Llama-3) to classify the headline.
        """
        if not self.featherless_api_key:
            logger.warning("FEATHERLESS_API_KEY not found. Using fallback.")
            return self.get_fallback_analysis(headline)

        headers = {
            "Authorization": f"Bearer {self.featherless_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        Analyze the following financial headline and determine if it represents a 'Systemic Warning' (risk to the whole market) or an 'Idiosyncratic/Neutral' event (specific to one firm or non-critical like a stock split).
        
        Headline: "{headline}"
        
        Respond ONLY with a JSON object in this format:
        {{
            "classification": "Systemic Warning" or "Idiosyncratic/Neutral",
            "reasoning": "A short sentence explaining why",
            "health_score": (Integer between 1 and 10, where 1 is total collapse and 10 is perfect health)
        }}
        """

        payload = {
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        try:
            response = requests.post(f"{self.featherless_base_url}/chat/completions", headers=headers, json=payload)
            result = response.json()
            
            if 'choices' not in result:
                error_msg = result.get('error', {}).get('message', 'Unknown error')
                logger.error(f"Featherless AI error: {error_msg}")
                # Switch to fallback if upgrade required or other API error
                return self.get_fallback_analysis(headline)
                
            content = result['choices'][0]['message']['content']
            import json
            import re
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return self.get_fallback_analysis(headline)
        except Exception as e:
            logger.error(f"Featherless AI analysis failed: {e}")
            return self.get_fallback_analysis(headline)

if __name__ == "__main__":
    analyzer = NewsAnalyzer()
    headlines = analyzer.fetch_headlines()
    for h in headlines:
        print(f"Headline: {h}")
        analysis = analyzer.analyze_risk(h)
        print(f"Analysis: {analysis}\n")
