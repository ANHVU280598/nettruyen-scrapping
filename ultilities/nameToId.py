import hashlib

def name_to_id(name):
    # Create a hash object
    hash_object = hashlib.md5(name.encode())
    
    # Get the hexadecimal representation of the hash
    hash_id = hash_object.hexdigest()
    
    return hash_id
