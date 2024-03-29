import platform

def get_device():
    if platform.system() == 'Darwin':
        return 'mps'
    return 'cpu'
