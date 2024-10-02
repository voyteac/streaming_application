import base64
import io
from typing import Tuple, List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

matplotlib.use('Agg')


def plot_figure_to_buffer(x_values_original: List[float],
                          y_values_original: List[float],
                          y_values: List[float],
                          online_predictions: List[Tuple[float, float]],
                          prediction_error_margin: float,
                          window_size: int,
                          detected_anomalies: List[int]) -> Tuple[str, List[float], List[float]]:
    # KPI VALUES LINE
    plt.figure(figsize=(12, 6))
    plt.plot(x_values_original, y_values_original, color='blue', label='KPI Values', linewidth=1)

    # KPI VALUES
    for i in range(len(online_predictions)):
        actual_color = 'red' if (i + window_size + 1) in detected_anomalies else 'green'
        plt.scatter(i + window_size + 1, online_predictions[i][1], color=actual_color, marker='x')

    # LEGEND
    plt.scatter([], [], color='red', marker='x', label='Actual Value (Anomaly)')
    plt.scatter([], [], color='green', marker='x', label='Actual Value (Normal)')

    # MARGIN
    lower_bound_values = [np.mean(y_values[i - window_size:i]) - prediction_error_margin for i in
                          range(window_size, len(y_values) - 1)]
    upper_bound_values = [np.mean(y_values[i - window_size:i]) + prediction_error_margin for i in
                          range(window_size, len(y_values) - 1)]

    lower_bound_values = np.round(lower_bound_values, 2)
    upper_bound_values = np.round(upper_bound_values, 2)

    plt.fill_between(range(window_size + 1, len(online_predictions) + window_size + 1), lower_bound_values,
                     upper_bound_values, color='red', alpha=0.2, label='Out of Range Margin')

    plt.xlabel('Samples')
    plt.ylabel('KPI Values')
    plt.title('KPI values predictions with detected anomalies')
    plt.legend()
    plt.grid(True)
    plt.ylim(50, 90)
    # plt.show()

    # SAVE TO BUFFER
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    matplotlib.pyplot.close()

    image_uri = f"data:image/png;base64,{image_base64}"

    return image_uri, lower_bound_values, upper_bound_values


def create_placeholder_if_no_plots() -> Figure:
    plt.figure()
    plt.plot([], [])
    return plt.gcf()
