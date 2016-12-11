import requests, json
data_dump=[]

old_data = dict()
old_data["nodes"]=[]
old_data["links"]=[]

def collect_info(api,source,data_dump): 
    resp = requests.get(api)

    nodes = [{"id": source,
                      "group": 1,
                     "info": "Democratic"}]
    links = []

    for i in resp.json()['records']:
        nodes.append({"id": i["Contributor"]["Contributor"],
                      "group": [1] if i ["Type_of_Contributor"]["Type_of_Contributor"]==u"Individual" else [0],
                     "info": i["Occupation"]["Occupation"]})
        links.append({"source": i["Contributor"]["Contributor"],
                     "target": source,
                     "value": i["Total_$"]["Total_$"],
                     "info": i ["Type_of_Contributor"]["Type_of_Contributor"],
                     "donation_year": i["Election_Year"]["Election_Year"]})

    return {"nodes": nodes+data_dump["nodes"], "links": links+data_dump["links"]}

old_data = collect_info("http://api.followthemoney.org/?c-t-eid=22511&gro=s,y,d-eid,d-occupation&APIKey=b0daa74a9cd146f3e5eef9cc477302b3&mode=json"
    ,"BASS KAREN R", old_data)
old_data = collect_info("http://api.followthemoney.org/?c-t-eid=40620386&gro=s,y,d-eid,d-occupation&APIKey=b0daa74a9cd146f3e5eef9cc477302b3&mode=json"
    ,"KAMALA D HARRIS", old_data)
old_data = collect_info("http://api.followthemoney.org/?c-t-eid=331199&gro=s,y,d-eid,d-occupation&APIKey=b0daa74a9cd146f3e5eef9cc477302b3&mode=json",
                       "KEVIN MCCARTHY", old_data)
print old_data
