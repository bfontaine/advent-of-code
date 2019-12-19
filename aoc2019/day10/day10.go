package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"sort"
)

type Coordinates struct {
	x, y int
}

func (c Coordinates) String() string {
	return fmt.Sprintf("(%v, %v)", c.x, c.y)
}

type Direction Coordinates

type Vision struct {
	origin Coordinates
	vision map[Direction][]Coordinates
}

func NewVision(origin Coordinates) *Vision {
	return &Vision{
		origin: origin,
		vision: make(map[Direction][]Coordinates),
	}
}

func (v *Vision) AddAsteroid(asteroid Coordinates) {
	direction, distance := v.origin.DirectionDistance(asteroid)

	asteroids := v.vision[direction]

	size := len(asteroids)

	if size == 0 {
		v.vision[direction] = []Coordinates{asteroid}
		return
	}

	// find the first that is further than the current one
	i := sort.Search(size, func(i int) bool {
		return v.origin.Distance(asteroids[i]) >= distance
	})

	if i == size {
		// not found: add at the end
		v.vision[direction] = append(asteroids, asteroid)
	}
	// TODO
}

func (v Vision) ClockwiseDirections() []Direction {
	directions := make([]Direction, 0, len(v.vision))

	// TODO

	return directions
}

func gcd(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func (cx Coordinates) Distance(cx2 Coordinates) int {
	x := cx2.x - cx.x
	y := cx2.y - cx.y

	factor := gcd(x, y)

	if factor < 0 {
		factor *= -1
	}

	return factor
}

func (cx Coordinates) DirectionDistance(cx2 Coordinates) (Direction, int) {
	x := cx2.x - cx.x
	y := cx2.y - cx.y

	factor := cx.Distance(cx2)

	// (0,0) -> (4,6) = (2,3)
	// (0,0) -> (4,5) = (4,5)
	// (0,0) -> (4,4) = (1,1)
	// (0,0) -> (4,3) = (4,3)
	// (0,0) -> (4,2) = (2,1)
	// (0,0) -> (4,1) = (4,2)
	// (0,0) -> (4,0) = (1,0)
	// (5,4) -> (3,2) = (-1,-1)
	//
	// (2,10) -> (4,5) = (-2,5)
	// (2,2) -> (0,0) = (-1, -1)
	return Direction{
		x / factor,
		y / factor,
	}, factor
}

func main() {
	if len(os.Args) != 3 {
		log.Fatal("Usage: day10 <1|2> <input.txt>")
		os.Exit(1)
	}
	problem := os.Args[1]
	input, err := ioutil.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}

	m := make(map[Coordinates]Vision)

	y := 0
	x := 0

	for _, chr := range input {
		coordinates := Coordinates{x, y}

		switch chr {
		case '\n':
			y++
			x = -1
		case '#':
			m[coordinates] = NewVision(coordinates)
		}
		x += 1
	}

	for asteroid1, vision1 := range m {
		for asteroid2, _ := range m {
			if asteroid1 == asteroid2 {
				continue
			}

			vision1.AddAsteroid(asteroid2)

			// fmt.Printf("%v -> %v : direction %v\n",
			// 	asteroid1, asteroid2, direction)

			// we don't care which asteroid we see, only how many
			vision1[direction]++
		}
	}

	var maxVision int
	var bestAsteroid Coordinates

	for asteroid, vision := range m {
		if len(vision) > maxVision {
			maxVision = len(vision)
			bestAsteroid = asteroid
		}
	}
	fmt.Printf("Best asteroid: %+v, it can detect %v asteroids\n", bestAsteroid, maxVision)
	if problem == "1" {
		return
	}

	vision := m[bestAsteroid]
	nth := 0

	for dir := range vision.ClockwiseDirections() {
		nth++

		if nth == 200 {
			//
		}
	}

	// TODO
}
