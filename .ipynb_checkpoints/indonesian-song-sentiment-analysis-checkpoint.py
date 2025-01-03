{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Indonesian Popular Song Lyrics Sentiment Analysis\n",
    "\n",
    "## Project Workflow\n",
    "1. Data Scraping\n",
    "2. Data Cleaning\n",
    "3. Data Labeling\n",
    "4. Model Training\n",
    "5. Sentiment Analysis\n",
    "6. Visualization of Results\n",
    "7. Data Export"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Install required libraries\n",
    "!pip install requests beautifulsoup4 pandas numpy scikit-learn nltk matplotlib seaborn transformers torch\n",
    "\n",
    "# Import required libraries\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import re\n",
    "import nltk\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Download Indonesian NLP resources\n",
    "nltk.download('punkt')\n",
    "nltk.download('stopwords')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Web Scraping Function for Indonesian Song Lyrics\n",
    "def scrape_indonesian_lyrics(artist=None, num_songs=10):\n",
    "    \"\"\"\n",
    "    Scrape Indonesian song lyrics from a lyrics website\n",
    "    \"\"\"\n",
    "    # Note: Replace with actual lyrics website URL\n",
    "    base_url = \"https://example-indonesian-lyrics-site.com\"\n",
    "    lyrics_data = []\n",
    "    \n",
    "    # Implement web scraping logic here\n",
    "    # This is a placeholder - you'll need to adapt to specific website structure\n",
    "    for _ in range(num_songs):\n",
    "        # Fetch song details\n",
    "        # Extract title, artist, lyrics\n",
    "        lyrics_data.append({\n",
    "            'title': 'Song Title',\n",
    "            'artist': 'Artist Name',\n",
    "            'lyrics': 'Actual song lyrics'\n",
    "        })\n",
    "    \n",
    "    return pd.DataFrame(lyrics_data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Data Cleaning Function\n",
    "def clean_lyrics(df):\n",
    "    \"\"\"\n",
    "    Clean and preprocess song lyrics\n",
    "    \"\"\"\n",
    "    def preprocess_text(text):\n",
    "        # Convert to lowercase\n",
    "        text = text.lower()\n",
    "        \n",
    "        # Remove special characters and numbers\n",
    "        text = re.sub(r'[^a-zA-Z\\s]', '', text)\n",
    "        \n",
    "        # Remove extra whitespaces\n",
    "        text = re.sub(r'\\s+', ' ', text).strip()\n",
    "        \n",
    "        return text\n",
    "    \n",
    "    # Apply preprocessing\n",
    "    df['cleaned_lyrics'] = df['lyrics'].apply(preprocess_text)\n",
    "    \n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. Data Labeling Function\n",
    "from textblob import TextBlob\n",
    "\n",
    "def label_sentiment(df):\n",
    "    \"\"\"\n",
    "    Label sentiment for Indonesian lyrics\n",
    "    Uses TextBlob for initial sentiment scoring\n",
    "    \"\"\"\n",
    "    def get_sentiment(text):\n",
    "        # Translate to English for better sentiment analysis\n",
    "        # Note: You might want to use a specialized Indonesian sentiment model\n",
    "        blob = TextBlob(text)\n",
    "        sentiment_score = blob.sentiment.polarity\n",
    "        \n",
    "        # Categorize sentiment\n",
    "        if sentiment_score > 0.05:\n",
    "            return 'Positive'\n",
    "        elif sentiment_score < -0.05:\n",
    "            return 'Negative'\n",
    "        else:\n",
    "            return 'Neutral'\n",
    "    \n",
    "    df['sentiment'] = df['cleaned_lyrics'].apply(get_sentiment)\n",
    "    df['sentiment_score'] = df['cleaned_lyrics'].apply(lambda x: TextBlob(x).sentiment.polarity)\n",
    "    \n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4. Machine Learning Model Training\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.naive_bayes import MultinomialNB\n",
    "from sklearn.metrics import classification_report\n",
    "\n",
    "def train_sentiment_model(df):\n",
    "    # Prepare data\n",
    "    X = df['cleaned_lyrics']\n",
    "    y = df['sentiment']\n",
    "    \n",
    "    # Split data\n",
    "    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
    "    \n",
    "    # Vectorization\n",
    "    vectorizer = TfidfVectorizer(max_features=5000)\n",
    "    X_train_vectorized = vectorizer.fit_transform(X_train)\n",
    "    X_test_vectorized = vectorizer.transform(X_test)\n",
    "    \n",
    "    # Train Naive Bayes Classifier\n",
    "    classifier = MultinomialNB()\n",
    "    classifier.fit(X_train_vectorized, y_train)\n",
    "    \n",
    "    # Evaluate\n",
    "    y_pred = classifier.predict(X_test_vectorized)\n",
    "    print(classification_report(y_test, y_pred))\n",
    "    \n",
    "    return classifier, vectorizer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 5. Sentiment Analysis Function\n",
    "def analyze_lyrics_sentiment(lyrics, model, vectorizer):\n",
    "    \"\"\"\n",
    "    Predict sentiment for new lyrics\n",
    "    \"\"\"\n",
    "    # Preprocess\n",
    "    cleaned_lyrics = clean_lyrics(pd.DataFrame({'lyrics': [lyrics]}))\n",
    "    \n",
    "    # Vectorize\n",
    "    vectorized_lyrics = vectorizer.transform(cleaned_lyrics['cleaned_lyrics'])\n",
    "    \n",
    "    # Predict\n",
    "    prediction = model.predict(vectorized_lyrics)\n",
    "    prediction_proba = model.predict_proba(vectorized_lyrics)\n",
    "    \n",
    "    return prediction[0], prediction_proba[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 6. Visualization Functions\n",
    "def plot_sentiment_distribution(df):\n",
    "    \"\"\"\n",
    "    Create visualizations of sentiment distribution\n",
    "    \"\"\"\n",
    "    plt.figure(figsize=(12,6))\n",
    "    \n",
    "    # Pie Chart\n",
    "    plt.subplot(1,2,1)\n",
    "    sentiment_counts = df['sentiment'].value_counts()\n",
    "    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')\n",
    "    plt.title('Sentiment Distribution')\n",
    "    \n",
    "    # Box Plot of Sentiment Scores\n",
    "    plt.subplot(1,2,2)\n",
    "    sns.boxplot(x='sentiment', y='sentiment_score', data=df)\n",
    "    plt.title('Sentiment Score Distribution')\n",
    "    \n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "def plot_artist_sentiment(df):\n",
    "    \"\"\"\n",
    "    Analyze sentiment by artist\n",
    "    \"\"\"\n",
    "    artist_sentiment = df.groupby('artist')['sentiment_score'].mean().sort_values(ascending=False)\n",
    "    \n",
    "    plt.figure(figsize=(10,6))\n",
    "    artist_sentiment.plot(kind='bar')\n",
    "    plt.title('Average Sentiment Score by Artist')\n",
    "    plt.xlabel('Artist')\n",
    "    plt.ylabel('Average Sentiment Score')\n",
    "    plt.xticks(rotation=45, ha='right')\n",
    "    plt.tight_layout()\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7. Data Export\n",
    "def export_results(df, filename='indonesian_song_sentiment_analysis.csv'):\n",
    "    \"\"\"\n",
    "    Export final analysis results\n",
    "    \"\"\"\n",
    "    df.to_csv(filename, index=False)\n",
    "    print(f\"Results exported to {filename}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Main Workflow\n",
    "def main():\n",
    "    # 1. Scrape Lyrics\n",
    "    lyrics_df = scrape_indonesian_lyrics()\n",
    "    \n",
    "    # 2. Clean Data\n",
    "    cleaned_df = clean_lyrics(lyrics_df)\n",
    "    \n",
    "    # 3. Label Sentiment\n",
    "    labeled_df = label_sentiment(cleaned_df)\n",
    "    \n",
    "    # 4. Train Model\n",
    "    model, vectorizer = train_sentiment_model(labeled_df)\n",
    "    \n",
    "    # 5. Visualize Results\n",
    "    plot_sentiment_distribution(labeled_df)\n",
    "    plot_artist_sentiment(labeled_df)\n",
    "    \n",
    "    # 6. Export Results\n",
    "    export_results(labeled_df)\n",
    "\n",
    "    return labeled_df, model, vectorizer\n",
    "\n",
    "# Run the main workflow\n",
    "if __name__ == '__main__':\n",
    "    results_df, sentiment_model, lyrics_vectorizer = main()"
   ]
  }
 ],
 "metadata": {
   "kernelspec": {
     "display_name": "Python 3",
     "language": "python",
     "name": "python3"
   },
   "language_info": {
     "name": "python",
     "version": "3.8.5"
   }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
