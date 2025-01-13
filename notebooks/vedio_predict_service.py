import torch
def preload_image_encoder(image,predictor):
    with torch.no_grad():
        image = image.to('cpu').float().unsqueeze(0)
        backbone_out = predictor.forward_image(image)
    return backbone_out