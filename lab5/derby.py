from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Participation:
    horse: int  # index of participating horse
    jockey: int  # index of participating jockey
