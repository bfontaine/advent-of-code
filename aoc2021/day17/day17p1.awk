{
    # target area: x=20..30, y=-10..-5
    split($3, x_range_text, "[.=,]")
    split($4, y_range_text, "[.=]")

    x1 = x_range_text[2]
    x2 = x_range_text[4]

    y1 = y_range_text[2]
    y2 = y_range_text[4]

    #  -- y2 --
    # |        |
    # x1       x2
    # |        |
    #  -- y1 --
    #
    #      -5
    #  20       30
    #      -10
    #
    # while x <= x2 && y >= y1
    # if x1 <= x and y2 >= y

    highest_of_all = 0

    min_xv1 = 0
    if (x1 < 0)
      min_xv1 = x1

    # YOLO
    for (xv1=min_xv1; xv1<=x2; xv1++) {
      for (yv1=y1; yv1<1000; yv1++) {
        x = 0
        y = 0
        highest = 0
        ok = 0

        xv = xv1
        yv = yv1

        # step
        while (x <= x2 && y >= y1) {
          y > highest ? highest = y : 0

          if (x1 <= x && y2 >= y) {
            ok = 1
            break
          }

          x += xv
          y += yv
          xv = xv > 0 ? xv-1 : xv < 0 ? xv+1 : 0
          yv -= 1

          if (x < x1 && xv == 0) {
            break
          }
        }
        if (ok) {
          highest > highest_of_all ? highest_of_all = highest : 0
        }
      }
    }

    print highest_of_all
}
