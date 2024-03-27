import torch

def checkgpu():
    mps = torch.backends.mps.is_available()
    gpu = torch.cuda.is_available()

    if mps:
        print("GPU available:", mps)
        return "mps"
    elif gpu:
        print("GPU available:", torch.cuda.get_device_name(0))
        return 0
    else:
        print('No GPU available')
        return "cpu"
