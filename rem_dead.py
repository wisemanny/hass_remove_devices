import os
import json

devices = None  # store core.device_registry
entities = None  # store core.entity_registry

# Define file names
FILE_DEV_REG = '.storage/core.device_registry'
FILE_ENT_REG = '.storage/core.entity_registry'

FILE_DEV_REG_BAK = FILE_DEV_REG + '.bak'
FILE_ENT_REG_BAK = FILE_ENT_REG + '.bak'

FILE_DEV_REG_UPD = FILE_DEV_REG + '.upd'
FILE_ENT_REG_UPD = FILE_ENT_REG + '.upd'

# Load registries
with open(FILE_DEV_REG, encoding='utf-8') as d:
    devices = json.load(d)

with open(FILE_ENT_REG, encoding='utf-8') as e:
    entities = json.load(e)

# Backup
with open(FILE_DEV_REG_BAK, 'w', encoding='utf-8') as d:
    json.dump(devices, d, indent=2, ensure_ascii=False)

with open(FILE_ENT_REG_BAK, 'w', encoding='utf-8') as e:
    json.dump(entities, e, indent=2, ensure_ascii=False)

# Find dead devices
dead_devices_id = []
dead_devices_index = []
for m, dev in enumerate(devices['data']['devices']):
    if 'name_by_user' in dev and dev['name_by_user'] is not None and \
            dev['name_by_user'].endswith('dead'):
        print(f'Found dead device {dev["name_by_user"]}')
        # save device id and its index in array to remove later
        dead_devices_id.append(dev['id'])
        dead_devices_index.append(m)

# Find entities for dead devices and remove them
for dev_id in dead_devices_id:
    print(f'\nProcess device with id {dev_id}:')
    del_entities_index = []
    for i, e in enumerate(entities['data']['entities']):
        if e['device_id'] == dev_id:
            print('Delete entity %s' % e['entity_id'])
            del_entities_index.append(i)
    # remove items from the end to not impact the indexes
    # print(del_entities)
    for k in del_entities_index[::-1]:
        entities['data']['entities'].pop(k)

# remove dead devices in reverse order
for n in dead_devices_index[::-1]:
    devices['data']['devices'].pop(n)

# save updated dict
with open(FILE_DEV_REG_UPD, 'w', encoding='utf-8') as d:
    json.dump(devices, d, indent=2, ensure_ascii=False)

with open(FILE_ENT_REG_UPD, 'w', encoding='utf-8') as e:
    json.dump(entities, e, indent=2, ensure_ascii=False)

# Run diff
print("Diff changes:")
DIFF_DEV = f'diff "{FILE_DEV_REG_UPD}" "{FILE_DEV_REG_BAK}"'
DIFF_ENT = f'diff "{FILE_ENT_REG_UPD}" "{FILE_ENT_REG_BAK}"'

print(DIFF_DEV)
os.system(DIFF_DEV)

print("")
print(DIFF_ENT)
os.system(DIFF_ENT)

print('Done')
