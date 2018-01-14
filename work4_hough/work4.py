from PIL import Image, ImageDraw
import math,cmath,numpy

def getpixel(x,y,image,num = 3):
    pixelArray = []
    width, height = image.size
    for i in range(-(int(num/2)),int(num/2)+1):
        if y + i < 0 or y + i >= height:
            continue
        for j in range(-(int(num/2)),int(num/2)+1):
            if x + j < 0 or x + j >= width :
                continue
            else:
                pixel = image.getpixel((x + j ,y + i))
                pixelArray.append(pixel)
    
    return(pixelArray)

def Sobel(x,y,image):
    pixel = getpixel(x,y,image)
    
    result = abs(-(pixel[0]) + pixel[2] - 2 * pixel[3] + 2 * pixel[5] - pixel[6] + pixel[8]) + \
            abs(-(pixel[0]) - 2 * pixel[1] - pixel[2] + pixel[6] + 2 * pixel[7] + pixel[8])
    
    if result > 255: result = 255 
    elif result < 0: result = 0
    return int(result) 

def Polar(x,y):
    complex = numpy.complex(x,y)
    polar = cmath.polar(complex)
    r = round(polar[0])
    deg = round(math.degrees(polar[1]))
    
    return (r,deg)

def Houghtranform(x,y,s):
    r = round(x * math.cos(math.radians(s)) + y * math.sin(math.radians(s)))
    
    return r

def main():
    image = Image.open( 'table.jpg' )
    # image.show()
    width, height = image.size

    GrayImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(GrayImage)

    for x in range(0, width):       
        for y in range(0, height):
            Grayscale = (image.getpixel((x,y))[0]+image.getpixel((x,y))[1]+image.getpixel((x,y))[2])/3
            draw.point((x,y), fill=(int(Grayscale)))
    # GrayImage.show()
    GrayImage.save( "GrayImage.jpg" )

    SobelImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(SobelImage)

    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = Sobel(x,y,GrayImage)
            draw.point((x,y), fill=(pixel))

    # SobelImage.show()
    SobelImage.save( "SobelImage.jpg" )

    pointArray = []
    rmax = 0
    for x in range(0, width):       
        for y in range(0, height):
            if (SobelImage.getpixel((x,y)) >= 200):
                (r,deg) = Polar(x,y)
                pointArray.append((x,y))
                if rmax < r : rmax = r
                    
    polar_dict = {}
    HoughImage = Image.new( "L", (361,rmax+1) , (0))  
    draw = ImageDraw.Draw(HoughImage)

    for point in pointArray:
        x = point[0]
        y = point[1]
        for s in range(-180,181):
            r = Houghtranform(x,y,s)
            polar_dict.setdefault((r,s),0)
            polar_dict[(r,s)] += 1
            draw.point((s + 180, int(r)), fill=(255))
    # HoughImage.show()
    HoughImage.save( "HoughImage.jpg" )

    polar_dict = sorted(polar_dict.items(), key=lambda x: x[1], reverse=True)

    maxpolar = polar_dict[0]

    ResultImage = Image.open( 'table.jpg' )
    draw = ImageDraw.Draw(ResultImage)
    r = maxpolar[0][0]
    s = maxpolar[0][1]
    for x in range(0, width):       
        for y in range(0, height):
            r_xy = Houghtranform(x,y,s)
            if r - 1 <= r_xy <= r + 1 :
            # if r_xy == r :
                draw.point((x,y), fill=(255,0,0))
            
    # ResultImage.show()
    ResultImage.save( "ResultImage.jpg" )

if __name__ == '__main__':
    main()