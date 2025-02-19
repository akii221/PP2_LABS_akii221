import json

print("Interface Status")
print("=========================================================================================")
print("{:<50} {:<20} {:<10} {:<5}".format("DN", "Description", "Speed", "MTU"))  
print("-------------------------------------------------- -------------------- -------  -------")

with open("sample-data.json", "r") as obj:
    data = json.load(obj)
    for object in data['imdata']:
        a = object['l1PhysIf']['attributes']['dn']
        b = object['l1PhysIf']['attributes']['descr']
        c = object['l1PhysIf']['attributes']['speed']
        d = object['l1PhysIf']['attributes']['mtu']

        print("{:<50} {:<20} {:<10} {}".format(a,b,c,d))