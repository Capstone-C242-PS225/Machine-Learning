import tensorflow as tf
import numpy as np
from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
import random

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

app = Flask(__name__)

model = tf.keras.models.load_model('addiction_predict.h5')

def classify(cluster):
    if cluster == 0:
        return 'ringan'
    elif cluster == 1:
        return 'sedang'
    elif cluster == 2:
        return 'berat'
    else:
        return 'sangat berat'

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()
    newRegister = data['newRegister']
    transaction_amount = data['transaction_amount']
    user_total_cashout = data['user_total_cashout']
    user_total_balance = data['user_total_balance']
    company_total_cashout = data['company_total_cashout']
    status_SUCCESS = 1
    try:
        company_total_balance_estimate = data['company_total_balance']
    except:
        company_total_balance_estimate = 10 * user_total_balance
    data_to_predict = np.array([[newRegister, transaction_amount, user_total_cashout, 
                                 user_total_balance, company_total_cashout, company_total_balance_estimate, status_SUCCESS]])
    
    scaler1 = joblib.load('scaler_standard.pkl')
    scaled_data1 = scaler1.transform(data_to_predict)  

    scaler2 =joblib.load('scaler_minmax.pkl')
    scaled_data2 = scaler2.transform(scaled_data1)

    input_data = np.array(scaled_data2)

    predictions = model.predict(input_data)
    predicted_classes = np.argmax(predictions, axis=1)

    result = {
        'predicted_addiction': classify(predicted_classes[0]),  
        'prediction_probabilities': predictions.tolist(),  
    }

    # Return the JSON response
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)