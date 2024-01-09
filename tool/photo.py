from PIL import Image

# 将白色及近似白色的地方转成透明
def changepixel(img):
    picture = Image.open(img).convert('RGBA')
    datas = picture.getdata()
    new_data = []
    for item in datas:

        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    picture.putdata(new_data)
    picture.save('new.png')

changepixel(r'test.jpg')


