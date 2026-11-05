import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from part1 import EN1
from part2 import EN2
from part3 import EN3

EN = {**EN1, **EN2, **EN3}
d = json.load(open(os.path.join(HERE, '..', 'works.json'), encoding='utf-8'))
missing = [x['slug'] for x in d if x['slug'] not in EN]
print('works:', len(d), 'translated:', len(EN), 'missing:', missing)
json.dump(EN, open(os.path.join(HERE, '..', 'works-en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
