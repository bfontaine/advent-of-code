package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
)

type Coordinates struct {
	x, y int
}

type Direction Coordinates

type Vision map[Direction]bool

func gcd(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func (cx Coordinates) DirectionTo(cx2 Coordinates) Direction {
	x := cx2.x - cx.x
	y := cx2.y - cx.y

	factor := gcd(x, y)

	if factor < 0 {
		factor *= -1
	}

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
	}
}

func main() {
	if len(os.Args) != 2 {
		log.Fatal("Usage: problem1 <input.txt>")
		os.Exit(1)
	}
	input, err := ioutil.ReadFile(os.Args[1])
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
			m[coordinates] = make(Vision)
		}
		x += 1
	}

	for asteroid1, vision1 := range m {
		for asteroid2, _ := range m {
			if asteroid1 == asteroid2 {
				continue
			}

			direction := asteroid1.DirectionTo(asteroid2)

			// fmt.Printf("%v -> %v : direction %v\n",
			// 	asteroid1, asteroid2, direction)

			// we don't care which asteroid we see, only how many
			vision1[direction] = true
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
}
