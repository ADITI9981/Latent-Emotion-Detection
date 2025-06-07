# 🌟 Latent Emotion Detection — Reveal the True Feelings Behind Text

Welcome to **Latent Emotion Detection**, an intelligent system designed to uncover hidden emotions within any text you provide! Whether it’s joy, sadness, anger, or surprise, this project uses advanced machine learning and natural language processing techniques to detect the subtle emotions beneath the surface.

## 🚀 Why This Project Rocks

- 🎯 **Deep Emotion Detection**  
  Goes beyond basic sentiment analysis to identify nuanced, latent emotions.

- 🔍 **Robust Text Preprocessing**  
  Cleans and prepares text data for accurate emotion classification.

- 🛠️ **Full-Stack Application**  
  Built with Flask to offer an interactive web interface complete with secure user authentication and persistent data storage.

- 🎨 **Engaging Visual Feedback**  
  Displays emojis and graphics that bring emotion detection results to life.

## 🗂️ What’s Inside

| File                 | Purpose                                               |
|----------------------|-------------------------------------------------------|
| `app.py`             | Main Flask application to run the web server and handle user requests |
| `Preprocessor.py`    | Cleans and processes text input for the model         |
| `Helper.py`          | Utility functions for data handling and prediction support |
| `auth.py`            | Manages user login and registration securely          |
| `database_setup.py`  | Initializes the database for user data                 |
| `emotion_dataset_raw.csv` | Raw dataset used for training and evaluation       |
| `text_emotion.pkl`   | Pretrained machine learning model for emotion detection |
| `stop_hinglish.txt`  | List of stopwords for text preprocessing               |
| `users.db`           | SQLite database storing user information               |
| Images               | Emojis and UI assets to enhance user experience        |

## ⚙️ How to Run

Ready to try it out? Follow these simple steps:

```bash
# Clone this repository
git clone https://github.com/ADITI9981/Latent-Emotion-Detection.git
cd Latent-Emotion-Detection

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python database_setup.py

# Start the Flask app
python app.py
Open your browser and visit http://localhost:5000 to start detecting emotions in your text!
