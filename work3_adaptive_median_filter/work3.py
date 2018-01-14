from PIL import Image, ImageDraw
import random

def getpixel(x,y,image,num = 3):
    pixelArray = []
    width, height = image.size
    for i in range(-(int(num/2)),int(num/2)+1):
        if y + i < 0 or y + i >= height:        #當超過圖片範圍則忽略
            continue
        for j in range(-(int(num/2)),int(num/2)+1):
            if x + j < 0 or x + j >= width :
                continue                        #當超過圖片範圍則忽略
            else:
                pixel = image.getpixel((x + j ,y + i))
                pixelArray.append(pixel)
    
    return(pixelArray)

def main():
    image = Image.open( '1.jpg' )
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
    
    NoiseImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(NoiseImage)

    for x in range(0, width):       
        for y in range(0, height):
            ram = random.random()
            if ram <= 0.25: pixel = 0
            elif ram <= 0.5: pixel = 255
            else: pixel = GrayImage.getpixel((x,y))
            
            draw.point((x,y), fill=(int(pixel)))

    # NoiseImage.show()
    NoiseImage.save( "NoiseImage.jpg" )

    MedianImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(MedianImage)

    for x in range(0, width):       
        for y in range(0, height):
            pixelArray = getpixel(x,y,NoiseImage,7)
            pixelArray.sort()
            med = pixelArray[int(len(pixelArray)/2) + 1]
            draw.point((x,y), fill=(med))

    # MedianImage.show()
    MedianImage.save( "MedianImage.jpg" )

    AdaptiveMedianImage = Image.new( "L", (width,height) , (0))  
    draw = ImageDraw.Draw(AdaptiveMedianImage)

    for x in range(0, width):       
        for y in range(0, height):
            for num in range(3,8,2):            #依序執行3, 5, 7
                pixelArray = getpixel(x,y,NoiseImage,num)
                pixelArray.sort()
                pixel_xy = NoiseImage.getpixel((x,y))
                
                pixel_min = pixelArray[0]
                pixel_med = pixelArray[int(len(pixelArray)/2) + 1]
                pixel_max = pixelArray[len(pixelArray) - 1]
                                 
                if pixel_min < pixel_med < pixel_max:
                    if pixel_min < pixel_xy < pixel_max:
                        draw.point((x,y), fill=(pixel_xy))    #(x,y)不是雜訊 直接輸出
                        break
                    else:
                        draw.point((x,y), fill=(pixel_med))   #(x,y)是雜訊 輸出med
                        break
                elif num == 7:
                    draw.point((x,y), fill=(pixel_xy))        #(x,y)位於黑白區域 直接輸出
                else: continue

    # AdaptiveMedianImage.show()
    AdaptiveMedianImage.save( "AdaptiveMedianImage.jpg" )

if __name__ == '__main__':
    main()