import os


def filer_generate_randomized(instance, filename):
    import uuid
    print(instance)
    uuid_str = str(uuid.uuid4())
    random_path = u"%s/%s/%s" % (uuid_str[0:2], uuid_str[2:4], uuid_str)
    name, extension = os.path.splitext(filename)
    filename = u'{}{}'.format(
        str(uuid.uuid4()), extension
    )
    return os.path.join(random_path, filename)
