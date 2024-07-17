from src.nlp_core.sentiment_analysis import SentimentAnalysis

def train_model():
    '''fungsi yang digunakan untuk melakukan pelatihan model'''
    sa = SentimentAnalysis()

    return sa.train_model()

def predict_sentiment(text):
    '''fungsi yang digunakan untuk melakukan prediksi sentiment'''
    sa = SentimentAnalysis()
    return sa.predict(text)