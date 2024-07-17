import pandas as pd

from src.nlp_core.text_preprocessing import TextProcessing

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import pickle

from src.utils.main_logger import log_data, log_error
from dotenv import dotenv_values

env = dotenv_values(".env")

class SentimentAnalysis:
    def __init__(self):
        self.dataset_path = env['DATASET_PATH']
        self.model_path = env['MODEL_PATH']
        self.dataset_name = env['TRAIN_DATASET_NAME']
        self.model_name = env['MODEL_NAME']
        self.vectorizer_name = env['VECTORIZER_NAME']
        self.project_path = env['PROJECT_PATH']

    def load_dataset(self, name):
        try:
            df = pd.read_csv(f"{self.project_path}{self.dataset_path}{name}")
            log_data(f"Data '{self.dataset_name}' berhasil dibaca.")
            return df
        except FileNotFoundError:
            log_error(f"File '{self.project_path}{self.dataset_path}{name}' not found.")
            return None
        
    def train_model(self):
        try:
            log_data("Memulai Tahap Pelatihan Model")
            df = self.load_dataset(self.dataset_name)
            df.dropna(inplace=True)

            # log_data("Membersihkan dataset")
            # tp = TextProcessing()
            # df["text_clean"] = df["Instagram Comment Text"].apply(tp.preprocessing_text)
            # df.to_csv(f"{self.project_path}{self.dataset_path}clean_dataset.csv")

            df.rename(
                columns={
                    "Sentiment":'sentiment',
                    "Instagram Comment Text":"text"
                },
                inplace=True
            )

            df.drop(columns=["Id"], axis=1,inplace=True)
            df.replace({
                "sentiment":{
                    "positive":1,
                    "neutral":0,
                    "negative":-1
                }
            },inplace=True)

            log_data("Menjalankan Proses TFIDF")
            vectorizer = TfidfVectorizer(max_features=2000)
            x = vectorizer.fit_transform(df["text_clean"]).toarray()
            y = df["sentiment"]

            log_data("Membagi Data Training dan Testing")
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

            log_data("Pelatihan")
            model = MultinomialNB()
            model.fit(X_train, y_train)

            log_data("Menyimpan Model")
            with open(f"{self.project_path}{self.model_path}{self.model_name}.pkl", "wb") as file:
                pickle.dump(model, file)
            with open(f"{self.project_path}{self.model_path}{self.vectorizer_name}.pkl", "wb") as file:
                pickle.dump(vectorizer, file)

            log_data("Model berhasil disimpan.")
            return "pelatihan model sukses"
        except Exception as e:
            log_error(f"Terdapat kesalahan pada proses pelatihan: {str(e)}")
            return "pelatihan model gagal"
        
    def predict(self, text):
        try:
            log_data("Memuat Model")
            with open(f"{self.project_path}{self.model_path}{self.model_name}.pkl", "rb") as file:
                model = pickle.load(file)
            with open(f"{self.project_path}{self.model_path}{self.vectorizer_name}.pkl", "rb") as file:
                vectorizer = pickle.load(file)

            log_data("Melakukan Prediksi")
            text_clean = TextProcessing().preprocessing_text(text)
            x = vectorizer.transform([text_clean]).toarray()
            prediction = model.predict(x)[0]

            if prediction == 0:
                sentiment = "netral"
            elif prediction == 1:
                sentiment = "positif"
            else:
                sentiment = "negatif"

            return sentiment
        except Exception as e:
            log_error(f"Terdapat kesalahan pada memuat model: {str(e)}")
            return "gagal melakukan prediksi"
