from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssistantState:
    name: str


class StateMachine:
    """Máquina de estados simple para el flujo de voz."""

    def __init__(self) -> None:
        self.current = AssistantState("IDLE")
        self.allowed = {
            "IDLE": {"LISTENING", "ERROR"},
            "LISTENING": {"PROCESSING", "IDLE", "ERROR"},
            "PROCESSING": {"SPEAKING", "IDLE", "ERROR"},
            "SPEAKING": {"IDLE", "LISTENING", "ERROR"},
            "ERROR": {"IDLE", "LISTENING"},
        }

    def transition(self, next_state: str) -> AssistantState:
        if next_state not in self.allowed.get(self.current.name, set()):
            raise ValueError(
                f"Transición inválida: {self.current.name} -> {next_state}. "
                f"Estados permitidos: {sorted(self.allowed.get(self.current.name, set()))}"
            )
        self.current = AssistantState(next_state)
        return self.current

    def reset(self) -> AssistantState:
        self.current = AssistantState("IDLE")
        return self.current
