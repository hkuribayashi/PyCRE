# Index
action = 76

total_actions = action + 1
int_part = total_actions // 7
remainder = total_actions % 7

if int_part > 0:
    bs_index = int_part - 1
else:
    bs_index = 0

if remainder == 0:
    new_action = 6
else:
    new_action = remainder - 1

print(bs_index)
print(new_action)
