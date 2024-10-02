import threading
import random


class KpiGenerator:
    def __init__(self, n, z, min_normal_value=60, max_normal_value=80, anomaly_diff=20, anomaly_days=5, precision=2,
                 max_diff_percent=1, normal_offset_min=0, normal_offset_max=5):
        # Initialization with parameters for KPI data generation
        self.n = n
        self.z = z
        self.min_normal_value = min_normal_value
        self.max_normal_value = max_normal_value
        self.anomaly_diff = anomaly_diff
        self.anomaly_days = anomaly_days
        self.precision = precision
        self.max_diff_percent = max_diff_percent
        self.normal_offset_min = normal_offset_min
        self.normal_offset_max = normal_offset_max
        self.current_index = 0
        self.lock = threading.Lock()

    def get_next_kpi_value(self, y_vals):
        # Safely retrieves the next KPI value in a loop.
        with self.lock:
            value = y_vals[self.current_index]
            self.current_index = (self.current_index + 1) % len(y_vals)  # Cycle through the list
        return value

    def generate_kpi_data(self, amount_of_the_samples=200, z=200, min_normal_value=60, max_normal_value=80,
                          anomaly_diff=5, anomaly_days=5, precision=2,
                          max_diff_percent=1, normal_offset_min=0,
                          normal_offset_max=5):
        """
        Generates KPI values with normal oscillation and occasional anomalies.
        """
        y_list = []  # Initialize list for KPI values
        num_complete_cycles = amount_of_the_samples // z
        remaining_samples = amount_of_the_samples % z
        half_cycle = z // 2

        # Generate normal KPI values for complete cycles
        for cycle in range(num_complete_cycles):
            for i in range(half_cycle):
                normal_value = min_normal_value + (max_normal_value - min_normal_value) * (i / half_cycle)
                max_diff = normal_value * (max_diff_percent / 100) + random.uniform(normal_offset_min,
                                                                                    normal_offset_max)
                y_list.append(round(normal_value + random.uniform(-max_diff, max_diff), precision))

            for i in range(half_cycle):
                normal_value = max_normal_value - (max_normal_value - min_normal_value) * (i / half_cycle)
                max_diff = normal_value * (max_diff_percent / 100) + random.uniform(normal_offset_min,
                                                                                    normal_offset_max)
                y_list.append(round(normal_value + random.uniform(-max_diff, max_diff), precision))

        # Generate values for remaining samples
        for i in range(remaining_samples):
            if i < half_cycle:
                normal_value = min_normal_value + (max_normal_value - min_normal_value) * (i / half_cycle)
            else:
                normal_value = max_normal_value - (max_normal_value - min_normal_value) * (
                            (i - half_cycle) / half_cycle)

            max_diff = normal_value * (max_diff_percent / 100) + random.uniform(normal_offset_min, normal_offset_max)
            y_list.append(round(normal_value + random.uniform(-max_diff, max_diff), precision))

        # Introduce anomalies at random intervals
        total_anomalies = amount_of_the_samples // 10  # Example: 10% of samples are anomalies
        anomaly_periods = []

        while total_anomalies > 0:
            start_day = random.randint(0, amount_of_the_samples - anomaly_days)
            if start_day + anomaly_days <= amount_of_the_samples:
                anomaly_periods.append((start_day, start_day + anomaly_days - 1))
                total_anomalies -= anomaly_days

        anomaly_periods.sort()  # Sort and merge anomaly periods
        merged_periods = []
        last_end = -1

        for start, end in anomaly_periods:
            if start > last_end:
                merged_periods.append((start, end))
                last_end = end
            elif end > last_end:
                merged_periods[-1] = (merged_periods[-1][0], end)
                last_end = end

        # Adjust KPI values for anomalies
        for start, end in merged_periods:
            for day in range(start, end + 1):
                original_value = y_list[day]
                y_list[day] = max(0, round(original_value - anomaly_diff, precision))  # Prevent negative values

        return y_list  # Return only KPI values

#
# kpi_gen = KpiGenerator(n=200, z=200)
# kpis = kpi_gen.generate_kpi_data()
# print(kpis)