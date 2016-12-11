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
    keep = {}
    
    new = {"links": [], "nodes": []}
    
    for n in orig['nodes']:
        if 1 in n['group']:
            keep[n['id']] = (random.random() < keep_fraction)
            parts = n['id'].split(' ')
            old_id = n['id']
            
            if parts[-1] == 'Jr':
                new_id = parts[1] + ' ' + parts[0] + ' Jr'
            else:
                new_id = people_map[n['id']] = ' '.join(parts[1:]) + ' ' + parts[0]
            
            people_map[n['id']] = new_id
    
    


    for n in orig['nodes']:
        if 0 in n['group']:
            keep[n['id']] = False
            for l in new['links']:
                if l['source'] == n['id'] and keep[l['target']]:
                    keep[n['id']] = True
                    break
    
    for l in orig['links']:
        if not keep[l['target']] and (l['source'] not in keep or not keep[l['source']]):
            continue
        
        if l['target'] in people_map:
            print "%s -> %s" % (l['target'], people_map[l['target']],)
            l['target'] = people_map[l['target']]
        new['links'].append(l)
               
        
    for n in orig['nodes']:
        if keep[n['id']] == True:
            if n['id'] in people_map:
                n['id'] = people_map[n['id']]
            new['nodes'].append(n)

        
    import json
    with open(fname+'.json', 'w') as outfile:
        json.dump(new, outfile, indent=5)
            
if __name__ == "__main__":
    clean_json('../data_examples/floridafinal.json')