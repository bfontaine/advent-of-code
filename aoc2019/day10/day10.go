package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"os"
	"sort"
)

// Coordinates represents (x,y) coordinates
type Coordinates struct {
	x, y int
}

func (cx Coordinates) String() string {
	return fmt.Sprintf("(%v, %v)", cx.x, cx.y)
}

// Direction represents a direction
type Direction Coordinates

// Vision represents the vision from an asteroid
type Vision struct {
	origin Coordinates
	vision map[Direction][]Coordinates
}

// Size return the number of visible asteroids
func (v Vision) Size() int {
	return len(v.vision)
}

// NewVision creates a new, empty vision from the given coordinates
func NewVision(origin Coordinates) *Vision {
	return &Vision{
		origin: origin,
		vision: make(map[Direction][]Coordinates),
	}
}

// AddAsteroid add one asteroid to a Vision object
func (v *Vision) AddAsteroid(asteroid Coordinates) {
	direction, distance := v.origin.DirectionDistance(asteroid)

	asteroids := v.vision[direction]

	size := len(asteroids)

	if size == 0 {
		v.vision[direction] = []Coordinates{asteroid}
		return
	}

	// find the first i so that asteroids[i] is further than the current one
	i := sort.Search(size, func(i int) bool {
		return v.origin.Distance(asteroids[i]) >= distance
	})

	if i == size {
		// not found: add at the end
		v.vision[direction] = append(asteroids, asteroid)
	} else if i == 0 {
		v.vision[direction] = append([]Coordinates{asteroid}, asteroids...)
	} else {
		v.vision[direction] = append(append(asteroids[:i-1], asteroid), asteroids[i:]...)
	}
}

// ClockDistance returns the distance of the direction as if it were an arm on
// a clock. This is a float64 that can be used for comparisons.
func ClockDistance(d Direction) float64 {
	// https://stackoverflow.com/a/2339510/735926

	//  -------> x
	// |
	// |   ^
	// V   | top = lowest y's
	// y

	// The offsets are mostly trial-and-error to get the correct scores around
	// the clock
	r := math.Atan2(float64(d.y), float64(d.x)) + math.Pi/2
	if r >= 0 {
		return r
	}
	return 2*math.Pi + r
}

// ClockwiseDirections returns all directions from a vision, clockwise
func (v Vision) ClockwiseDirections() []Direction {
	directions := make([]Direction, len(v.vision))

	i := 0

	for direction := range v.vision {
		directions[i] = direction
		i++
	}

	sort.Slice(directions, func(i, j int) bool {
		return ClockDistance(directions[i]) < ClockDistance(directions[j])
	})

	fmt.Printf("sorted: %+v\n", directions)

	return directions
}

// LazerTo fires a lazer in some direction to crush an asteroid
func (v *Vision) LazerTo(d Direction) *Coordinates {
	vision, ok := v.vision[d]
	if !ok {
		return nil
	}

	coordinates := vision[0]

	v.vision[d] = vision[1:]

	return &coordinates
}

func gcd(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

// Distance computes a distance between two coordinates
// Distances can only be compared on the same direction.
func (cx Coordinates) Distance(cx2 Coordinates) int {
	x := cx2.x - cx.x
	y := cx2.y - cx.y

	factor := gcd(x, y)

	if factor < 0 {
		factor *= -1
	}

	return factor
}

// DirectionDistance returns both the direction and the distance between two
// coordinates
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

	m := make(map[Coordinates]*Vision)

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
		x++
	}

	for asteroid1, vision1 := range m {
		for asteroid2 := range m {
			if asteroid1 == asteroid2 {
				continue
			}

			vision1.AddAsteroid(asteroid2)
		}
	}

	var maxVision int
	var bestAsteroid Coordinates

	for asteroid, vision := range m {
		if vision.Size() > maxVision {
			maxVision = vision.Size()
			bestAsteroid = asteroid
		}
	}
	fmt.Printf("Best asteroid: %+v, it can detect %v asteroids\n", bestAsteroid, maxVision)
	if problem == "1" {
		return
	}

	vision := m[bestAsteroid]
	nth := 0

	for _, direction := range vision.ClockwiseDirections() {
		nth++

		crushed := vision.LazerTo(direction)

		if crushed != nil {
			fmt.Printf("The %dth asteroid to be vaporized is at %v (direction %v)\n",
				nth, crushed, direction)

			if nth == 200 {
				fmt.Printf("Solution: %v\n",
					crushed.x*100+crushed.y)
				break
			}
		}
	}
}
