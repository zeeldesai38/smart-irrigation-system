# Smart Irrigation System Using Machine Learning and AI Chatbot

## About the Project
This project predicts irrigation requirements using machine learning and provides an AI chatbot to answer agriculture-related questions. It helps users understand irrigation needs and learn about water-saving practices.

## Features
- Predicts irrigation requirements as **Low, Medium, or High**.
- Uses machine learning models for classification.
- Uses Gradient Boosting as the selected prediction model.
- Integrates an AI chatbot powered by Ollama and Llama 3.2 (1B).
- Uses Streamlit for the user interface.
- Uses ONNX Runtime to run the trained model.

## Dataset
The project uses the Irrigation Water Requirement Prediction Dataset from Kaggle.

Dataset link: https://www.kaggle.com/datasets/miadul/irrigation-water-requirement-prediction-dataset

The dataset contains 10,000 records with 19 input features and one target column, `Irrigation_Need`.

## Technologies Used
- Python
- Pandas and NumPy
- Scikit-learn
- Streamlit
- Ollama
- Llama 3.2 (1B)
- ONNX and ONNX Runtime

## Model Performance
The selected Gradient Boosting model achieved the following reported results:

- **Accuracy:** 99.7%
- **Macro F1-score:** 0.9831
- **High-class recall:** 91.04%


## Future Improvements
- Integrate real-time soil moisture and weather data.
- Connect sensors such as ESP32 for field monitoring.
- Add a Retrieval-Augmented Generation (RAG) system to provide answers grounded in agricultural documents.
- Explore automated irrigation control.



