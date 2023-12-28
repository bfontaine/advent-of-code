from typing import List, Iterator, Tuple, Optional


class Grid:
    """
    Basic grid container based on a list of strings.

    This exposes ``rows`` and ``columns`` attributes; each one is re-computed if the other one changes.
    """

    def __init__(self, rows: List[str]):
        self.rows = rows

    def copy(self):
        return self.__class__(rows=self.rows)

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        return self.rows == other.rows

    @property
    def height(self):
        return len(self._rows)

    @property
    def width(self):
        return len(self._rows[0])

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value: List[str]):
        self._rows = value
        self._columns = [
            "".join([row[x] for row in self.rows])
            for x in range(self.width)
        ]

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value: List[str]):
        self._columns = value
        self._rows = [
            "".join([column[y] for column in self.columns])
            for y in range(self.height)
        ]

    def valid_coordinates(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height

    @classmethod
    def from_string(cls, s: str):
        return cls(rows=s.splitlines())

    def iter_chars(self, char: Optional[str] = None) -> Iterator[Tuple[int, int]]:
        no_char = char is None
        for y, row in enumerate(self.rows):
            for x, c in enumerate(row):
                if no_char or c == char:
                    yield x, y
