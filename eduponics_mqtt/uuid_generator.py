import uuid

# make a UUID based on the host ID and current time, best option.
uuid_x = uuid.uuid1()
print(uuid_x)

# make a UUID using an MD5 hash of a namespace UUID and a name
uuid_y = uuid.uuid3(uuid.NAMESPACE_DNS, 'steminds.com')
print(uuid_y)

# make a random UUID
uuid_z = uuid.uuid4()
print(uuid_z)
