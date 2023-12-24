from typing import List


class Grid:
    """
    Basic grid container based on a list of strings.
    """

    def __init__(self, rows: List[str]):
        self.rows = rows

        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.columns = [
            "".join([row[x] for row in self.rows])
            for x in range(self.width)
        ]

    @classmethod
    def from_string(cls, s: str):
        return cls(rows=s.splitlines())
