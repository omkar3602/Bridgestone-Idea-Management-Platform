import uuid
keys = []
i = 0
while i < 9:
    key = uuid.uuid4().hex[:32].lower()
    if key in keys:
        continue
    else:
        keys.append(key)
        i += 1
print(keys)