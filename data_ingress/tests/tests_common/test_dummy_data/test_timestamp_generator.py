import pytest
from datetime import datetime
from data_ingress.common.dummy_data.timestamp_generator import RealTimestampGenerator


@pytest.mark.django_db
def test_get_formatted_timestamp(monkeypatch):
    time_gen = RealTimestampGenerator()
    timestamp = 1630454400
    monkeypatch.setattr('time.time', lambda: timestamp)

    expected = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    result = time_gen.get_formatted_timestamp()

    assert result == expected