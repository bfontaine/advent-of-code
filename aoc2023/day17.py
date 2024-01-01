from heapq import heappush, heappop, heapify
from typing import NamedTuple, List, Set, Tuple

import aoc
from aoc.containers import IntGrid
from aoc.directions import Direction, SOUTH, EAST, Orientation


class PositionState(NamedTuple):
    x: int
    y: int
    direction: Direction
    steps: int

    @property
    def coordinates(self):
        return self.x, self.y

    def forward(self):
        x1, y1 = self.direction.apply(self.x, self.y)
        return PositionState(x=x1, y=y1, direction=self.direction, steps=self.steps + 1)

    def turn(self, orientation: Orientation):
        new_direction = self.direction.turn(orientation)
        x1, y1 = new_direction.apply(self.x, self.y)
        return PositionState(x=x1, y=y1, direction=new_direction, steps=1)


class City(IntGrid):
    @property
    def end_position(self):
        return self.width - 1, self.height - 1

    def get_least_heat_loss(self, *, min_steps_per_direction: int, max_steps_per_direction: int):
        # (heat so far (used to prioritize so we always explore the path with min cost so far first), state)
        queue: List[Tuple[int, PositionState]] = []

        for direction in (EAST, SOUTH):
            x, y = direction.apply(0, 0)
            if self.valid_coordinates(x, y):
                position = PositionState(x=x, y=y, direction=direction, steps=1)
                queue.append((self.rows[y][x], position))

        heapify(queue)

        seen: Set[PositionState] = set()
        end_position = self.end_position

        heat: int
        position: PositionState
        candidate_positions: List[PositionState]
        while queue:
            heat, position = heappop(queue)

            if position in seen:
                continue
            seen.add(position)
            candidate_positions = []

            if position.steps >= min_steps_per_direction:
                if position.coordinates == end_position:
                    return heat

                # turn if we can
                candidate_positions.extend([
                    position.turn(orientation)
                    for orientation in Orientation
                ])

            # go forward if we can
            if position.steps < max_steps_per_direction:
                candidate_positions.append(position.forward())

            for candidate_position in candidate_positions:
                if self.valid_coordinates(candidate_position.x, candidate_position.y):
                    next_heat = heat + self.rows[candidate_position.y][candidate_position.x]
                    heappush(
                        queue,
                        (next_heat, candidate_position)
                    )


def problem1(text: str):
    city = City.from_string(text)
    return city.get_least_heat_loss(
        min_steps_per_direction=0,
        max_steps_per_direction=3,
    )


def problem2(text: str):
    city = City.from_string(text)
    return city.get_least_heat_loss(
        min_steps_per_direction=4,
        max_steps_per_direction=10,
    )


if __name__ == '__main__':
    aoc.run(problem1, problem2)
