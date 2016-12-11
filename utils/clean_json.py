import json
import random

def read_file(fname):
    with open(fname, 'r') as myfile:
        data=myfile.read()
    return data
    
def clean_json(fname, keep_fraction = 0.5):
    import json
    orig = json.load(open(fname, 'r'))
    people_map = {}
    people_keep = {}
    
    new = {"links": [], "nodes": []}
    
    for n in orig['nodes']:
        if ' ' in n['id']:
            people_keep[n['id']] = (random.random() < keep_fraction)
            
            if people_keep[n['id']]: 
                parts = n['id'].split(' ')
                if parts[-1] == 'Jr':
                    people_map[n['id']] = n['id'] = parts[1] + ' ' + parts[0] + ' Jr'
                else:
                    people_map[n['id']] = n['id'] = ' '.join(parts[1:]) + ' ' + parts[0]
                new['nodes'].append(n)
        else:
            new['nodes'].append(n)
            
    for l in orig['links']:
        if l['target'] not in people_keep:
            continue
        
        if l['target'] in people_map:
            l['target'] = people_map[l['target']]
        new['links'].append(l)
        
    import json
    with open(fname, 'w') as outfile:
        json.dump(new, outfile, indent=5)
            
if __name__ == "__main__":
    clean_json('../data_examples/floridafinal.json')