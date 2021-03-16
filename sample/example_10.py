counter = 1
for x in range(-500, 600, 100):
    for y in range(-500, 600, 100):
        if x != 0  and y != 0:
            print("{} [{}, {}]".format(counter, x, y))
            counter += 1
