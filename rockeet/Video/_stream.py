"""
Copyright (c) 2022 Philipp Scheer
"""


import cv2
import time
import gzip

from rockeet import logger


"""
If you have an image img (which is a numpy array) you can convert it into string using:

>>> img_str = cv2.imencode('.jpg', img)[1].tostring()
>>> type(img_str)
 'str'
Now you can easily store the image inside your database, and then recover it by using:

>>> nparr = np.fromstring(STRING_FROM_DATABASE, np.uint8)
>>> img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
where you need to replace STRING_FROM_DATABASE with the variable that contains the result of your query to the database containing the image.
"""


def stream(inputDeviceId: int = 0, rollingFrameRateCount: int = 30):
    video = cv2.VideoCapture(inputDeviceId)
    previousFrame = None

    rollingFrameRate = [1]

    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    frameWidth = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    framesPerSecond = int(video.get(cv2.CAP_PROP_FPS))

    logger.debug(f"recording in {frameWidth}x{frameHeight} ({framesPerSecond} fps)")

    while True:
        # start measuring frame rate
        start = time.time()

        # perform computation
        hasFrame, frame = video.read()
        if not hasFrame:
            break
        frame = cv2.flip(frame, 1)
        compressedFrame = cv2.imencode('.jpg', frame)[1].tostring()
        
        # print("jpgLen", len(compressedFrame))
        # print("compressedLen", len(gzip.compress(frame.tostring())))
        # differences = (frame-previousFrame) if previousFrame is not None else None
        previousFrame = frame

        # the differences are compressed and sent over the network
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        rollingFrameRate.append(time.time() - start)
        rollingFrameRate = rollingFrameRate[-rollingFrameRateCount:]
        print(f"frameRate: {rollingFrameRateCount/sum(rollingFrameRate) :.0f}")

    video.release()
    cv2.destroyAllWindows()
