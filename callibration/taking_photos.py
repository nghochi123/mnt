import cv2

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# set new dimensionns to cap object (not cap)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "./images/image_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
