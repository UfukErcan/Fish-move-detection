import cv2
import time



fps_start_time = 0
fps = 24

cap = cv2.VideoCapture("fishes.mp4")
cap1 = cv2.VideoCapture("fishes.mp4")
cap1.set(1,5)
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

#fps sabitlendi , videolar yakalandi , arkaplan ayirma fonksiyonu cagirildi.

# font
font = cv2.FONT_HERSHEY_SIMPLEX
# fontScale
fontScale = 1  
# Blue color in BGR
color = (255, 0, 0) 
# Line thickness of 2 px
thickness = 2


i =0
t=0
g = 0
bound_box_list = []
bound_box_list2 = []

#balik konumlarinin yazilacagi bound box listler olusturuldu , videodaki yazilarin kalinlik/renk degerleri tanimlandi

def convert(list):
    return tuple(list)


while(True):
    ret,frame = cap.read()
    ret,frame2 = cap1.read()
#while dongusu ile ana programa girildi. ret frame kodlari ile goruntuden anlik kareleri islemek icin cekiyoruz.

    if ret == False:
        print("Uyarı")
        
    #1
    fgmask = fgbg.apply(frame)  
    median = cv2.medianBlur(fgmask, 13)
    (contours, hierarchy) = cv2.findContours(median.copy(),cv2.RETR_EXTERNAL  , cv2.CHAIN_APPROX_SIMPLE )
    background = cv2.resize(median,(600,360))
    cv2.imshow("back",background)
    #2
    fgmask2 = fgbg.apply(frame2)  
    median2 = cv2.medianBlur(fgmask2, 13)
    (contour, hierarchy) = cv2.findContours(median2.copy(),cv2.RETR_EXTERNAL  , cv2.CHAIN_APPROX_SIMPLE )
   
   
#yukaridaki kodlarda ise cekmis oldugumuz karelere arkaplan ayirma islemi uyguluyoruz , daha sonra median filtreden geciriyoruz. 
#son olarak da konturlari tanimliyoruz, boylece videodaki baliklar gurultu azaltilip tespit ediliyor.


    #1


    for c in contours:
        if cv2.contourArea(c)<200:
            continue
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,255,255),3)
        cv2.circle(frame,(int(x+w/2),int(y+h/2)),2,(255,255,255),-1)
        

        #videoya filtre uygulanmasinin ardindan tespit edilen baliklar kareler icerisine aliniyor. Daha sonra asagidaki kodlar ile bound box listesi
        #icerisine konumlari kaydediliyor. Bu konumlari ileride hareket tespiti amacli kullanacagiz.

        
        bound_box_list.append([int(x+w/2),(y+h/2)])
        #print(bound_box_list)
        # org
        org = (x, y)   
        #frame1 = cv2.putText(frame, 'Hareket Ediyor', org, font, 
                   #fontScale, color, thickness, cv2.LINE_AA)
        #print(bound_box_list[i])
        i +=1

    
        #2
        for ct in contour:
            if cv2.contourArea(ct)<200:
                continue
            (a,b,c,d) = cv2.boundingRect(ct)
            cv2.rectangle(frame2, (a,b), (a+c, b+d), (255,255,255),3)
            bound_box_list2.append([int(a+c/2),(b+d/2)])
            #print(bound_box_list2)
            # org
            org2 = (a, b)
            #print(bound_box_list2[t])
            #t +=1

        if True :
            #asagidaki kisim ise ,programda baliklari tespit ettigimiz kisim. Bound box listesindeki konumlarin x veya y degerlerinde belli bir miktardan
            #fazla degisim varsa balik hareket ediyor yazdirilacak , eger degisim yoksa hareket etmiyor yazdirilacaktir.
            if bound_box_list2[g][0]-500<bound_box_list[g][0] and bound_box_list[g][0]<bound_box_list2[g][0] +500:
                if bound_box_list2[g][1]-500<bound_box_list[g][1] and bound_box_list[g][1]<bound_box_list2[g][1] +500:
                  
                    #print(bound_box_list)
                    #print("hareketlipic")
                    frame2 = cv2.putText(frame, 'Hareket ediyor', org, font, 
                               fontScale, (0,255,0), thickness, cv2.LINE_AA)
                    frame2 = cv2.resize(frame2,(600,400))
                    #cv2.imshow("frame23",frame2)
            else:
                frame2 = cv2.putText(frame, 'Hareket Etmiyor', org, font, 
                           fontScale, (0,0,255), thickness, cv2.LINE_AA)
                frame2 = cv2.resize(frame2,(600,400))
                #cv2.imshow("frame234",frame2)
                
            g = g+1


    frame1 = cv2.resize(frame,(600,400))
    #median = cv2.resize(median,(600,400))
    frame2 = cv2.resize(frame2,(600,400))
    #cv2.imshow("backgroun",median)
    #cv2.imshow("frame",frame1)
    cv2.imshow("frame2",frame2)



    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
    
        
cap.release()
cv2.destroyAllWindows()