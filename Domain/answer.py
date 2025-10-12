from __future__ import annotations

class Answer:
    def __init__(self, question_id: str, value: str) -> None:
        self.question_id = question_id
        self.value = value

    def __repr__(self) -> str:  # útil em logs/tests
        return f"Answer(question_id={self.question_id!r}, value={self.value!r})"
