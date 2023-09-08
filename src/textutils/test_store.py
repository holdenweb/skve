
"""
Testing database
"""
import json

with open("data.json") as j_data:
    in_data = json.load(j_data)

data = {}
for item in in_data:
    data[item['name']] = item

def people_matching(s):
    return [data[k] for k in data if s.lower() in k.lower()]

def update_person(p: dict, kv: dict):
    p.update(kv)
    data[p['name']] = p

if __name__ == '__main__':
    for result, letters in( (2, 'teoln'), (1, 'bprasv'), (0, 'xyz')):
        for letter in letters:
            assert len(people_matching(letter)) == result
    for letters, person in (('bpr', p2), ('hsd', p1)):
        for letter in letters:
            pm = people_matching(letter)
            assert len(pm) == 1
            assert pm[0] is person
