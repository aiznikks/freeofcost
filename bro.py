import torch.nn as nn

class FSRCNN(nn.Module):
    def __init__(self, upscale_factor):
        super(FSRCNN, self).__init__()
        self.first_part = nn.Sequential(
            nn.Conv2d(1, 56, 5, 1, 2),
            nn.PReLU(56)
        )

        self.mid_part = nn.Sequential(
            nn.Conv2d(56, 12, 1),
            nn.PReLU(12),
            nn.Conv2d(12, 12, 3, 1, 1),
            nn.PReLU(12),
            nn.Conv2d(12, 12, 3, 1, 1),
            nn.PReLU(12),
            nn.Conv2d(12, 12, 3, 1, 1),
            nn.PReLU(12),
            nn.Conv2d(12, 56, 1),
            nn.PReLU(56)
        )

        self.last_part = nn.ConvTranspose2d(56, 1, 9, stride=upscale_factor, padding=3, output_padding=upscale_factor - 1)

    def forward(self, x):
        x = self.first_part(x)
        x = self.mid_part(x)
        x = self.last_part(x)
        return x