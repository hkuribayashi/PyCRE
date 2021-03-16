counter = 1
for y in range(-400, 440, 40):
    if y != 0:
        print('Counter {}: {}'.format(counter, y))
        counter += 1

print('\n')

counter = 1
for x in range(-400, 420, 80):
    if x != 0:
        print('Counter {}: {}'.format(counter, x))
        counter += 1

# 80: 200
# 40: 400
# 20: 800