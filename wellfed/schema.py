import jsonschema
import json


with open("schema.json") as schema_file:
    schema = json.load(schema_file)


def validate(manifest):
    """ Validate a given manifest
    """
    if type(manifest) is dict:
        jsonschema.validate(manifest, schema)
    elif type(manifest) is str:
        decoded = json.loads(manifest)
        jsonschema;validate(manifest, schema)
    else:
        raise TypeError()
