import torch
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image

def get_human_details(image_path):
    # Load the pre-trained Mask R-CNN model
    model = maskrcnn_resnet50_fpn(pretrained=True)
    model = model.eval()

    # Load the image
    image = Image.open(image_path)
    image_tensor = F.to_tensor(image).unsqueeze(0)

    if torch.cuda.is_available():
        image_tensor = image_tensor.cuda()
        model = model.cuda()

    # Get the model's predictions
    with torch.no_grad():
        predictions = model(image_tensor)

    # Get the details of the detected humans
    humans = []
    for i, label in enumerate(predictions[0]['labels']):
        if label == 1:  # 1 is the label for person in COCO dataset
            try:
                # Get the coordinates of the bounding box
                box = predictions[0]['boxes'][i].cpu().numpy()
                x, y, width, height = box

                # Calculate the center coordinates
                center_x = x + width / 2
                center_y = y + height / 2

                # Get the color of the center pixel
                color = image_tensor[0, :, int(center_y), int(center_x)].cpu().numpy()

                # Add the details to the list of humans
                humans.append({"center": (center_x, center_y), "color": color})
            except Exception as e:
                print(f"get_human_details: Error while processing human: {e}")
                pass

    return humans

if __name__ == '__main__':
    humans = get_human_details('test/test.jpg')

    for human in humans:
        print(human)

    pass
