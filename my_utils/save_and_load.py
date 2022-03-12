import pickle

def save_and_load(file_name, data = None):
    if data == None:
        with open(file_name, 'rb') as f:
            return(pickle.loads(f.read()))
    
    with open(file_name, 'wb') as f:
        f.write(pickle.dumps(data))






