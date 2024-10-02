import numpy as np
from typing import List, Tuple
from sklearn.linear_model import LinearRegression

from common.logging_.to_log_file import log_debug


def detect_anomalies(x_values, y_values, window_size: int, prediction_error_margin: int) -> Tuple[List[float], List[float], List[float], List[Tuple[float, float]], List[int]]:
    model = LinearRegression()
    online_predictions = []
    detected_anomalies = []

    y_values_original = y_values.copy()
    x_values_original = x_values.copy()

    for i in range(window_size, len(y_values) - 1):
        X_train = np.array(y_values[i - window_size:i]).reshape(1, -1)
        y_train = np.array([y_values[i]])

        model.fit(X_train, y_train)

        predicted_value = model.predict(X_train)[0]
        actual_value = y_values[i + 1]

        lower_bound = np.mean(X_train) - prediction_error_margin
        upper_bound = np.mean(X_train) + prediction_error_margin

        online_predictions.append((predicted_value, actual_value))

        if actual_value < lower_bound or actual_value > upper_bound:
            log_debug(detect_anomalies,
                      f"Anomaly detected at sample {i + 1}: Predicted = {predicted_value:.2f}, Actual = {actual_value:.2f} (Out of range!)")
            detected_anomalies.append(i + 1)
        else:
            log_debug(detect_anomalies,
                      f"Sample {i + 1}: Predicted = {predicted_value:.2f}, Actual = {actual_value:.2f} (Within range)")

    return x_values_original, y_values_original, y_values, online_predictions, detected_anomalies

