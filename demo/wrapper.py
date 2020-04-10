import torch
import torch.nn as nn
import torchvision
import PIL


class Resnet18Embedding(nn.Module):
    def __init__(self, embedding_dimension=128, pretrained=False, normalized=True):
        super(Resnet18Embedding, self).__init__()
        self.embedding_dimension = embedding_dimension
        self.normalized = normalized
        self.model = torchvision.models.resnet18(pretrained=pretrained)
        input_features_fc_layer = self.model.fc.in_features
        # Output embedding
        self.model.fc = nn.Linear(input_features_fc_layer, embedding_dimension)
        self.fine_tuning = True

    def l2_norm(self, input):
        """Perform l2 normalization operation on an input vector.
        code copied from liorshk's repository: https://github.com/liorshk/facenet_pytorch/blob/master/model.py
        """
        input_size = input.size()
        buffer = input.pow(2)
        normp = buffer.sum(dim=1).add_(1e-10)
        norm = normp.sqrt()
        _output = torch.div(input, norm.view(-1, 1).expand_as(input))
        output = _output.view(input_size)
        return output

    def forward(self, images):
        """Forward pass to output the embedding vector (feature vector) after l2-normalization and multiplication
        by scalar (alpha)."""
        embedding = self.model(images)
        if self.normalized:
            embedding = 10 * self.l2_norm(embedding)
        return embedding


class Wrapper():
    def __init__(self):
        self.model = Resnet18Embedding()
        self.model.load_state_dict(torch.load("./best_state_dict.tar"))
        self.model.eval()
        self.transform = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def calculate_similarity(self, image1, image2):
        # image1, image2: Pillow image
        image1 = self.transform(image1)
        image2 = self.transform(image2)
        with torch.no_grad():
            batch = torch.stack([image1, image2], dim=0)
            embeddings = self.model.forward(batch)
            distance = torch.norm(embeddings[0] - embeddings[1])
            return float(10 / (10 + distance))


def main():
    wrapper = Wrapper()
    path1 = "./img/2 (4).jpg"
    path2 = "./img/2 (1).jpg"
    img1 = PIL.Image.open(path1)
    img2 = PIL.Image.open(path2)
    print(wrapper.calculate_similarity(img1, img2))


if __name__ == "__main__":
    main()
