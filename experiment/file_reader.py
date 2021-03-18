file_name = 'pi_digits'

with open(file_name) as f:
    lines = f.readlines()

for line in lines:
    print(line.rstrip())