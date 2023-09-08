
"""
Testing database
"""
data = {
    'Steve Holden': (p1 := {
        "name": "Steve Holden",
        "one": "the",
        "two": "quick",
        "three": "fox",
        "four": "jumps",
        "five": "over",
        "six": "the",
        "seven": "lazy",
        "eight": "dog",
        "two_a": "brown"
    }),
    'Napoleon Bonaparte': (p2 := {
        'name': 'Napoleon Bonaparte',
        'able': 1,
        'was': 2,
        'I': 3,
        'ere': 4,
        'saw': 6,
        'Elba': 7
    })
}

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
