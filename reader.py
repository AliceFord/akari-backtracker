from PIL import Image
import main

def findRawBorders(im: Image.Image):
    # left border
    width, height = im.size
    xL = 0
    while True:
        exit = False
        for i in range(height):
            if im.getpixel((xL, i))[0] > 150:
                exit = True
                break
        
        if exit: break
        xL += 1

    xR = width - 1
    while True:
        exit = False
        for i in range(height):
            if im.getpixel((xR, i))[0] > 150:
                exit = True
                break
        
        if exit: break
        xR -= 1

    yT = 0
    while True:
        exit = False
        for i in range(width):
            if im.getpixel((i, yT))[0] > 150:
                exit = True
                break
        
        if exit: break
        yT += 1

    yB = height - 1
    while True:
        exit = False
        for i in range(width):
            if im.getpixel((i, yB))[0] > 150:
                exit = True
                break
        
        if exit: break
        yB -= 1

    return (xL, yT, xR, yB)

def identifySquare(imIn: Image.Image):
    # First try to identify pink
    # rgb(227, 132, 224) = pink
    for x in range(imIn.width):
        for y in range(imIn.height):
            if 190 <= imIn.getpixel((x, y))[0] <= 260 and 100 <= imIn.getpixel((x, y))[1] <= 160 and 190 <= imIn.getpixel((x, y))[2] <= 250:
                return 0
            
    # cheeky crop
    im = imIn.crop((12, 12, imIn.width - 12, imIn.height - 12))
    # im.show()

    # find average colour WITHOUT white / black - check for empty square
    avg = (0, 0, 0)
    pixelCount = 0
    for x in range(im.width):
        for y in range(im.height):
            pixel = im.getpixel((x, y))
            if pixel[0] < 200 and pixel[1] < 200 and pixel[2] < 200 and pixel[0] > 50 and pixel[1] > 50 and pixel[2] > 50:
                avg = (avg[0] + pixel[0], avg[1] + pixel[1], avg[2] + pixel[2])
                pixelCount += 1

    if pixelCount >= (im.width * im.height) // 2:  # need at least half the pixels to be the right colour
        avg = (avg[0] / pixelCount, avg[1] / pixelCount, avg[2] / pixelCount)

        if (50 <= avg[0] <= 140 and 65 <= avg[1] <= 140 and 80 <= avg[2] <= 180):
            return 6

    # beam down centre
    blocks = 0
    inBlock = False
    for y in range(im.height):
        pixel = im.getpixel((im.width // 2, y))
        if pixel[0] > 230:
            if not inBlock:
                inBlock = True
                blocks += 1
        else:
            if inBlock:
                inBlock = False

    if inBlock:
        blocks -= 1
    if blocks > 0:
        return blocks

    # find "average" colour
    avg = (0, 0, 0)
    for x in range(im.width):
        for y in range(im.height):
            pixel = im.getpixel((x, y))
            avg = (avg[0] + pixel[0], avg[1] + pixel[1], avg[2] + pixel[2])

    avg = (avg[0] / (im.width * im.height), avg[1] / (im.width * im.height), avg[2] / (im.width * im.height))
    if avg[0] < 50 and avg[1] < 50 and avg[2] < 50:
        return 5
    # rgb(95, 110, 137) or rgb(79, 93, 115)
    # if (71 <= avg[0] <= 103 and 85 <= avg[1] <= 118 and 107 <= avg[2] <= 145):
    # return 6
    
    print(avg)

    im.show()
    raise Exception("OOPSIEEEEE")

def mainFn():
    X = 10
    Y = 10

    im = Image.open("archive/179.png")
    borders = findRawBorders(im)
    im = im.crop(borders)
    width, height = im.size
    grid = []

    # print(identifySquare(im.crop((2 * (width // X), 7 * (height // Y), (2+1) * (width // X), (7+1) * (height // Y)))))

    for x in range(X):
        grid.append([])
        for y in range(Y):
            grid[x].append(identifySquare(im.crop((y * (width // X), x * (height // Y), (y+1) * (width // X), (x+1) * (height // Y)))))

    # print(grid)
    main.solve(grid)    


if __name__ == "__main__":
    mainFn()