package main

import "testing"

func TestNewVision(t *testing.T) {
	v := NewVision(Coordinates{0, 0})
	if v == nil {
		t.Error("NewVision should not return nil")
	}
	if size := v.Size(); size != 0 {
		t.Errorf("Empty vision should be of size 0, not %v", size)
	}
}

func TestAddAsteroid(t *testing.T) {
	//   0  1  2  3  4  5
	// 0       b
	// 1
	// 2             x
	// 3
	// 4    a        c
	// 5             d
	// 6             e  f
	//
	// a, b, c, f are visible

	v := NewVision(Coordinates{4, 2})
	for _, cx := range []Coordinates{
		{1, 4},
		{2, 0},
		{4, 4},
		{4, 5},
		{4, 6},
		{5, 6},
	} {
		v.AddAsteroid(cx)
	}

	expectedSize := 4 // a/b/c/f

	if size := v.Size(); size != expectedSize {
		t.Errorf("Vision should be of size %v, not %v", expectedSize, size)
	}
}

func TestClockDistance(t *testing.T) {
	hours := []Direction{
		{0, -1},   // ^ noon
		{1, -1},   // / 1-2
		{1, 0},    // > 3
		{1, 1},    // \ 4-5
		{0, 1},    // v 6
		{-1, 1},   // / 7-8
		{-1, 0},   // < 9
		{-1, -1},  // \ 10-11
		{-1, -10}, // some point before midnight
	}
	for i, hourAfter := range hours {
		if i == 0 {
			continue
		}
		hour := hours[i-1]

		hourDistance := ClockDistance(hour)
		hourAfterDistance := ClockDistance(hourAfter)

		if hourDistance > hourAfterDistance {
			t.Errorf("Hour %v (%v, %.2f) should be < hour %v (%v, %.2f)",
				i-1, hour, hourDistance,
				i, hourAfter, hourAfterDistance,
			)
		}
	}
}
