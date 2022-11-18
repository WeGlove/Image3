import os

import matplotlib
import numpy


def iter(i):
    file = "cat.bmp"
    for j in range(i):
        width = 1197
        height = os.path.getsize(file) // 3 // width + 1

        img = numpy.zeros((height, width, 3), dtype=numpy.uint8)

        with open(file, "rb") as f:
            for i in range(os.path.getsize(file)):
                y = (i // 3) // width
                x = (i // 3) % width
                c = i % 3
                byte = f.read(1)
                img[y, x, c] = int.from_bytes(byte, "little")

        from PIL import Image
        # import numpy as np

        img = Image.fromarray(img, 'RGB')
        file = f'my{j}.bmp'
        img.save(file)


def once():
    import PIL
    file = "how_to_vorkurs.pdf"
    width = 1080
    height = os.path.getsize(file)//3//width + 1

    img = numpy.zeros((height, width, 3), dtype=numpy.uint8)

    with open(file, "rb") as f:
        for i in range(os.path.getsize(file)):
            y = (i//3) // width
            x = (i//3) % width
            c = i % 3
            byte = f.read(1)
            img[y, x, c] = int.from_bytes(byte, "little")

    from PIL import Image
    #import numpy as np

    img = Image.fromarray(img, 'RGB')
    img.save('my.bmp')
    img.show()

if __name__ == "__main__":
    once()
