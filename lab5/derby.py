from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RaceTrack:
    horses: frozenset[int]  # qualified horses in this race track
    jockeys: frozenset[int]  # licensed jockeys in this race track

@dataclass(frozen=True, slots=True)
class Participation:
    horse: int  # index of participating horse
    jockey: int  # index of participating jockey
