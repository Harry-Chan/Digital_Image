from PIL import Image, ImageDraw
from sympy import *
import time

def equation(x1,y1,x11,y11,x2,y2,x22,y22,x3,y3,x33,y33):

    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    d = Symbol('d')
    e = Symbol('e')
    f = Symbol('f')
    
    f1 = x11*a + y11*b + c - x1
    f2 = x22*a + y22*b + c - x2
    f3 = x33*a + y33*b + c - x3

    sol1 = solve((f1, f2, f3), a, b, c)
    
    f4 = x11*d + y11*e + f - y1
    f5 = x22*d + y22*e + f - y2
    f6 = x33*d + y33*e + f - y3
    
    sol2 = solve((f4, f5, f6), d, e, f)
    
    return sol1[a], sol1[b], sol1[c], sol2[d], sol2[e], sol2[f]

def bilinear(x,y,image):
    
    l = int(x)
    k = int(y)
    a = x - l
    b = y - k
    
    R = (1-a) * (1-b) * image.getpixel((l,k))[0] + a * (1-b) * image.getpixel((l+1,k))[0] + \
    (1-a) * b * image.getpixel((l,k+1))[0] + a * b * image.getpixel((l+1,k+1))[0]

    G = (1-a) * (1-b) * image.getpixel((l,k))[1] + a * (1-b) * image.getpixel((l+1,k))[1] + \
    (1-a) * b * image.getpixel((l,k+1))[1] + a * b * image.getpixel((l+1,k+1))[1]

    B = (1-a) * (1-b) * image.getpixel((l,k))[2] + a * (1-b) * image.getpixel((l+1,k))[2] + \
    (1-a) * b * image.getpixel((l,k+1))[2] + a * b * image.getpixel((l+1,k+1))[2]

    return R,G,B

def main():
  
    image = Image.open( 'P2.jpg' )  #需旋轉的圖
    image2 = Image.open( 'P1.jpg' ) #原圖
    width, height = image.size
    width2, height2 = image2.size

    a, b, c, d, e, f = equation(x1,y1,x11,y11,x2,y2,x22,y22,x3,y3,x33,y33)      #使用函式解出a,b,c,d,e,f

    newImage = Image.new( "RGB", (width2 * 3,height2 * 3) , (255, 255, 255))  #新建一個原圖長寬各三倍大的圖
    draw = ImageDraw.Draw(newImage)                                           

    for new_x in range(-(width2) + 1, width2 * 2 - 1):        #迴圈開始畫圖，從負的像素開始到2倍的像素停止
        for new_y in range(-(height2) + 1, height2 * 2 - 1):
                      
            if 0 <= new_x <= width2 - 1 and 0 <= new_y <= height2 - 1:  #如果在原圖範圍直接畫上原圖的像素值
                draw.point((new_x + width2, new_y + height2), fill=(image2.getpixel((new_x,new_y))))            
                                                                    #將像素位置加上長寬後再畫
                                                                    #使旋轉後超出原圖的像素點可以畫上
            else:
                x = (a * new_x) + (b * new_y) + c                   #不在原圖範圍內
                y = (d * new_x) + (e * new_y) + f                   #先經過affine tranform計算
                
                if 0 <= x <= width - 1 and 0 <= y <= height - 1:    #算出來的x,y範圍在需旋轉圖的寬高內                                                                                                                       
                    R,G,B = bilinear(x,y,image)                     #進行bilinear後將像素值畫上圖
                    draw.point((new_x + width2, new_y + height2), fill=(int(R),int(G),int(B)))  
                else:
                    continue
                   
    newImage.save( "output.jpg" )       #輸出圖片


if __name__ == '__main__':
    main()