from PIL import Image, ImageDraw
def getpixel(x,y,image,num = 3):
    pixelArray = []
    for i in range(-(int(num/2)),int(num/2)+1):
        for j in range(-(int(num/2)),int(num/2)+1):
            pixel = image.getpixel((x + j ,y + i))
            pixelArray.append(pixel)
    
    return(pixelArray)

def Laplacian(x,y,image):
    pixel = getpixel(x,y,image)
    
    result = 8 * pixel[4] - (pixel[0] + pixel[1] + pixel[2] + pixel[3] + pixel[5] + pixel[6] + pixel[7] + pixel[8])
    
    if result > 255: result = 255 
    elif result < 0: result = 0
    return int(result)

def Sobel(x,y,image):
    pixel = getpixel(x,y,image)
    
    result = abs(-(pixel[0]) + pixel[2] - 2 * pixel[3] + 2 * pixel[5] - pixel[6] + pixel[8]) + \
            abs(-(pixel[0]) - 2 * pixel[1] - pixel[2] + pixel[6] + 2 * pixel[7] + pixel[8])
    
    if result > 255: result = 255 
    elif result < 0: result = 0
    return int(result)  

def Blur(x,y,image):
    pixel = getpixel(x,y,image)
    
    result = (pixel[0] + pixel[1] + pixel[2] + pixel[3] + pixel[4] + pixel[5] + pixel[6] + pixel[7] + pixel[8]) / 9

    if result > 255: result = 255 
    elif result < 0: result = 0
    return int(result) 

def main():
    image = Image.open( 'dog.jpg' )
    width, height = image.size

    GrayImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(GrayImage)

    for x in range(0, width):       
        for y in range(0, height):
            Grayscale = (image.getpixel((x,y))[0]+image.getpixel((x,y))[1]+image.getpixel((x,y))[2])/3
            draw.point((x,y), fill=(int(Grayscale)))
    # GrayImage.show()
    GrayImage.save( "GrayImage.jpg" )

    LaplacianImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(LaplacianImage)

    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = Laplacian(x,y,GrayImage)
            draw.point((x,y), fill=(pixel))

    # LaplacianImage.show()
    LaplacianImage.save( "LaplacianImage.jpg" )

    SharpenNoiseImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(SharpenNoiseImage)

    for x in range(0, width):       
        for y in range(0, height):
            pixel = GrayImage.getpixel((x,y)) + LaplacianImage.getpixel((x,y))
            if pixel > 255: pixel = 255 
            elif pixel < 0: pixel = 0
            draw.point((x,y), fill=(pixel))
            
    # SharpenNoiseImage.show()
    SharpenNoiseImage.save( "SharpenNoiseImage.jpg" )

    SobelImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(SobelImage)

    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = Sobel(x,y,GrayImage)
            draw.point((x,y), fill=(pixel))
            
    # SobelImage.show()
    SobelImage.save( "SobelImage.jpg" )

    BlurImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(BlurImage)

    for x in range(1, width - 1):       
        for y in range(1, height - 1):
            pixel = Blur(x,y,SobelImage)
            draw.point((x,y), fill=(pixel))
            
    # BlurImage.show()
    BlurImage.save( "BlurImage.jpg" )

    NormalizationImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(NormalizationImage)

    for x in range(0, width):       
        for y in range(0, height):
            pixel = (BlurImage.getpixel((x,y)) / 255) * SharpenNoiseImage.getpixel((x,y))
            if pixel > 255: pixel = 255 
            elif pixel < 0: pixel = 0
            draw.point((x,y), fill=(int(pixel)))
            
    # NormalizationImage.show()
    NormalizationImage.save( "NormalizationImage.jpg" )

    SharpenImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(SharpenImage)

    for x in range(0, width):       
        for y in range(0, height):
            pixel = GrayImage.getpixel((x,y)) + NormalizationImage.getpixel((x,y))
            if pixel > 255: pixel = 255 
            elif pixel < 0: pixel = 0
            draw.point((x,y), fill=(pixel))
            
    # SharpenImage.show()
    SharpenImage.save( "SharpenImage.jpg" )


if __name__ == '__main__':
    main()