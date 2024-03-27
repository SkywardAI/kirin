import platform

# import torch


def get_device():
    if platform.system() == "Darwin":
        return "mps"
    # elif torch.cuda.is_available():
    #     return 'cuda'
    return "cpu"
