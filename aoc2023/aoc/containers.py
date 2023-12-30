from typing import List, Iterator, Tuple, Optional, Generic, TypeVar, Iterable, Sequence

T = TypeVar('T')


class AbstractGrid(Generic[T]):
    def __init__(self, rows: Iterable[Sequence[T]]):
        self._rows: List[Sequence[T]] = []
        self._columns: List[Sequence[T]] = []

        self.rows = list(rows)

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
    def rows(self, value: List[Sequence[T]]):
        self._rows = value
        self._columns = [
            self._compact_cells([row[x] for row in self.rows])
            for x in range(self.width)
        ]

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value: List[Sequence[T]]):
        self._columns = value
        self._rows = [
            self._compact_cells([column[y] for column in self.columns])
            for y in range(self.height)
        ]

    def _compact_cells(self, cells: List[T]) -> Sequence[T]:
        return cells

    @classmethod
    def _parse_row(cls, s: str) -> Sequence[T]:
        raise NotImplementedError()

    def copy(self):
        return self.__class__(rows=self.rows)

    def valid_coordinates(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height

    def iter_coordinates(self, seed: Optional[T] = None) -> Iterator[Tuple[int, int]]:
        no_seed = seed is None
        for y, row in enumerate(self.rows):
            for x, c in enumerate(row):
                if no_seed or c == seed:
                    yield x, y

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.rows == other.rows

    @classmethod
    def from_string(cls, s: str):
        return cls(
            rows=[
                cls._parse_row(row_str)
                for row_str in s.splitlines()
            ]
        )


class StringGrid(AbstractGrid[str]):
    """
    Basic grid container based on a list of strings.

    This exposes ``rows`` and ``columns`` attributes; each one is re-computed if the other one changes.
    """

    def _compact_cells(self, cells):
        return "".join(cells)

    @classmethod
    def _parse_row(cls, s):
        return s


class IntGrid(AbstractGrid[int]):
    @classmethod
    def _parse_row(cls, s):
        return [int(c) for c in s]
