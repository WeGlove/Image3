import math

import PIL.ImageOps
from PIL import Image, ImageDraw


def jpgify(fp, ratios):
    img = Image.open(fp)

    for i, (scale, quality, _) in enumerate(ratios):
        print(f"resizing Image {i}")
        resize_img = img.resize((round(img.width*scale), round(img.height*scale)))
        resize_img.save(f"tmp\\resize\\out_{i}.jpg", "JPEG", quality=round(quality), optimize=True, progressive=True)

    stack_img = Image.new("RGBA", (img.width, img.height))
    for i, (_, _, radius_ratio) in enumerate(ratios):
        print(f"stacking Image {i}")

        shape_img = Image.new("RGB", (img.width, img.height))
        draw = ImageDraw.Draw(shape_img)
        draw.ellipse(((img.width/2-img.width/2*radius_ratio, img.height/2-img.height/2*radius_ratio),
                      (img.width/2+img.width/2*radius_ratio, img.height/2+img.height/2*radius_ratio)),
                     fill=(255, 255, 255), outline=(0, 0, 0))
        shape_img = PIL.ImageOps.invert(shape_img)
        resize_img = Image.open(f"tmp\\resize\\out_{i}.jpg")
        upsize_img = resize_img.resize((img.width, img.height), resample=PIL.Image.NEAREST)
        upsize_img.putalpha(shape_img.convert("L"))

        stack_img.paste(upsize_img, (0,0), upsize_img)
        # shape_img.save(f"tmp\\masks\\out_{i}.jpg", "PNG")
        # stack_img.save(f"tmp\\stacks\\out_{i}.jpg", "PNG")
    stack_img.save(f"tmp\\out.png", "PNG")


if __name__ == '__main__':
    enums = 10
    curve_scale = 3
    curve_quality = 5
    bound = 0.01
    input = []
    for x in range(1, enums+1):
        i = enums+1 - x
        scale = ((i/enums)*(1-bound))**curve_scale + bound
        quality = (i/enums)**curve_quality*100
        radius_ratio = math.sqrt(2)*(x-1)/enums
        input.append((scale, quality, radius_ratio))
    print(input)
    jpgify("in.png", input)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
