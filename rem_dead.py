import json

devices = None # store core.device_registry
entities = None # store core.entity_registry

with open('.storage/core.device_registry', encoding='utf-8') as d:
    devices = json.load(d)

with open('.storage/core.entity_registry', encoding='utf-8') as e:
    entities = json.load(e)

# Backup
with open('.storage/core.device_registry.bak', 'w', encoding='utf-8') as d:
    json.dump(devices, d, indent=2, ensure_ascii=False)

with open('.storage/core.entity_registry.bak', 'w', encoding='utf-8') as e:
    json.dump(entities, e, indent=2, ensure_ascii=False)

# Find dead devices
dead_devices_id = []
dead_devices_index = []
for m in range(0, len(devices['data']['devices'])):
    dev = devices['data']['devices'][m]
    if 'name_by_user' in dev and dev['name_by_user'] != None and \
            dev['name_by_user'].endswith('dead'):
        print(f'Found dead device {dev["name_by_user"]}')
        # save device id and its index in array to remove later
        dead_devices_id.append(dev['id'])
        dead_devices_index.append(m)

# Find entities and remove
for dev_id in dead_devices_id:
    print(f'\nProcess device with id {dev_id}:')
    del_entities_index = []
    for i in range(0, len(entities['data']['entities'])):
        e = entities['data']['entities'][i]
        if e['device_id'] == dev_id:
            print('Delete entity %s' % e['entity_id'])
            del_entities_index.append(i)
    # remove items from the end to not impact the indexes
    #print(del_entities)
    for k in del_entities_index[::-1]:
        entities['data']['entities'].pop(k)


# remove devices in reverse order
for n in dead_devices_index[::-1]:
    devices['data']['devices'].pop(n)


# save updated dict
with open('.storage/core.device_registry.upd', 'w', encoding='utf-8') as d:
    json.dump(devices, d, indent=2, ensure_ascii=False)

with open('.storage/core.entity_registry.upd', 'w', encoding='utf-8') as e:
    json.dump(entities, e, indent=2, ensure_ascii=False)
