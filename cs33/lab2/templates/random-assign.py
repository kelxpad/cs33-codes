import random

assign = ["Aaron", "Klex"]
pset_qs_first_half = [1, 4]
pset_qs_second_half = [6, 7] # hand gestures

random.shuffle(assign)
random.shuffle(pset_qs_first_half)
random.shuffle(pset_qs_second_half)

for i in range(2):
    person = assign.pop()
    q1 = pset_qs_first_half.pop()
    q2 = pset_qs_second_half.pop()
    print(f"{person} gets {q1} and {q2}")