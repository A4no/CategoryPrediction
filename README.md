CategoryPrediction

This project is a news classification system that combines web scraping, machine learning, and a Telegram bot. The system automatically collects news articles from the aravot.am website using Selenium, builds a dataset from the scraped data, and trains a machine learning model to classify news into categories.

Project Overview

The scraper collects hundreds or thousands of news articles and their corresponding categories. After gathering the data, it is processed and used to train a RandomForestClassifier model. The trained model can predict the category of new news texts.

Users can interact with the system through a Telegram bot. When a user sends a news text, the bot processes the message, runs the trained model, and returns the predicted category.

Categories

The model predicts one of the following categories:

Legal

Sport

Culture

Politics

Technologies Used

Python

Selenium (for web scraping)

Scikit-learn (RandomForestClassifier)

Pandas / NumPy (data processing)

Telegram Bot API

Workflow

Selenium scrapes news articles from aravot.am.

The collected data is combined into a dataset.

The dataset is used to train a RandomForestClassifier model.

A Telegram bot allows users to send news text.

The model predicts the category and returns the result to the user.

Example Output

User sends a news article to the bot:

Prediction: Politics
Author

Arno Emeksuzyan
Aspiring ML / AI Developer
