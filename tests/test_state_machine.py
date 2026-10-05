import pytest
from voice_assistant.latency import LatencyLogger
from voice_assistant.state_machine import StateMachine


def test_state_machine_transitions_valid() -> None:
    machine = StateMachine()
    assert machine.current.name == "IDLE"
    assert machine.transition("LISTENING").name == "LISTENING"
    assert machine.transition("PROCESSING").name == "PROCESSING"
    assert machine.transition("SPEAKING").name == "SPEAKING"
    assert machine.transition("IDLE").name == "IDLE"


def test_state_machine_rejects_invalid_transition() -> None:
    machine = StateMachine()
    with pytest.raises(ValueError):
        machine.transition("SPEAKING")


def test_latency_logger_records_and_summarizes() -> None:
    logger = LatencyLogger()
    logger.record("stt", logger.entries[0].started_at if logger.entries else __import__("datetime").datetime.now(__import__("datetime").timezone.utc), __import__("datetime").datetime.now(__import__("datetime").timezone.utc), True, "ok")
