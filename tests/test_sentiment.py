import pytest
from engine import VaderSentimentEngine

def test_analyze_message_positive():
    engine = VaderSentimentEngine()
    text = "I absolutely love this service! It's fantastic."
    label, score = engine.analyze_message(text)
    assert label == "Positive"
    assert score > 0.05

def test_analyze_message_negative():
    engine = VaderSentimentEngine()
    text = "This is terrible. I am very angry and disappointed."
    label, score = engine.analyze_message(text)
    assert label == "Negative"
    assert score < -0.05

def test_analyze_message_neutral():
    engine = VaderSentimentEngine()
    text = "The package arrived on Tuesday."
    label, score = engine.analyze_message(text)
    assert label == "Neutral"

def test_conversation_trend_improving():
    engine = VaderSentimentEngine()
    # First half negative, second half positive
    messages = [
        {"text": "I am angry", "sentiment_score": -0.8},
        {"text": "This is bad", "sentiment_score": -0.6},
        {"text": "Okay, that helps", "sentiment_score": 0.2},
        {"text": "Thank you, great job", "sentiment_score": 0.9}
    ]
    analysis = engine.analyze_conversation(messages)
    assert analysis["trend"] == "Improving"

def test_conversation_trend_declining():
    engine = VaderSentimentEngine()
    # First half positive, second half negative
    messages = [
        {"text": "Hello, good morning", "sentiment_score": 0.5},
        {"text": "I have an issue", "sentiment_score": -0.2},
        {"text": "This is useless", "sentiment_score": -0.8}
    ]
    analysis = engine.analyze_conversation(messages)
    assert analysis["trend"] == "Declining"
