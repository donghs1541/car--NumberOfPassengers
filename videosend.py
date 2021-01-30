import cv2
import socket
import numpy
from threading import Thread
import time
from multiprocessing import Process, Queue

def receive(s,signal_queue):  #멀티프로세스를 이용하여 항시 데이터를 받는것을 대기함
    while True:
        recvData = s.recv(1024)
        signal_queue.put(recvData.decode()) #받은 데이터를 Queue에 삽입함


if __name__== "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## server ip, port
    s.connect(('127.0.0.1', 20001))
    cam2 = cv2.VideoCapture('1.mp4')   #0번캠
    #cam2 = cv2.VideoCapture(1) #1번캠
    cam = cv2.VideoCapture(0) #저장돼있는 영상 전송
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    cam2.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cam2.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    signal_queue = Queue(10) #큐 선언 최대크기 1개
    process1 = Process(target=receive, args=(s, signal_queue))#멀티프로세스 선언
    process1.start() #멀티프로세스 시작
    signal = '1'
    while True:
        try:
            signal = signal_queue.get_nowait()  #큐의 값을꺼냄
        except:
            pass
        if signal == "2" and cam2.isOpened(): #signal 2 즉 두번쨰 카메라 신호를 받으면
            ret2, frame2 = cam2.read()
            if ret2:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

                result, frame2 = cv2.imencode('.jpg', frame2, encode_param)
                # frame을 String 형태로 변환
                data = numpy.array(frame2) #이미지 변환
                stringData = data.tostring() #이미지 string으로 변환
                s.sendall((str(len('a'))).encode().ljust(16) + str('a').encode())
                s.sendall((str(len(stringData))).encode().ljust(16) + stringData) #이미지 전송
                print("두번째 카메라 완료")
                signal = '1'
            else:
                break
        elif signal == "1" and cam.isOpened():
            ret, frame = cam.read()

            if ret:
                cv2.imshow('', frame)
                if cv2.waitKey(1) == ord('q'):  # q to quit
                    raise StopIteration

                ## 0~100에서 90의 이미지 품질로 설정 (default = 95)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

                ## encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
                result, frame = cv2.imencode('.jpg', frame, encode_param)
                # frame을 String 형태로 변환
                data = numpy.array(frame)
                stringData = data.tostring()

                # 서버에 데이터 전송
                s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
            else:
                break

    s.close()
    print("카메라 종료")
    cam.release()
    cam2.release()
'''
while True:
    signal = signal_queue.get()

    if signal == "2" and cam2.isOpened():
        print("두번째 카메라 전송")
        ret2, frame2 = cam2.read()
        if ret2:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

            result, frame2 = cv2.imencode('.jpg', frame2, encode_param)
            # frame을 String 형태로 변환
            data = numpy.array(frame2)
            stringData = data.tostring()

            s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    elif signal == "1" and cam.isOpened():
        ret, frame = cam.read()

        cv2.imshow('', frame)
        if cv2.waitKey(1) == ord('q'):  # q to quit
            raise StopIteration

        if ret:
            ## 0~100에서 90의 이미지 품질로 설정 (default = 95)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

            ## encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            # frame을 String 형태로 변환
            data = numpy.array(frame)
            stringData = data.tostring()

            # 서버에 데이터 전송
            s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
cam.release()
cam2.release()


    while True:
        if signal_queue.full() == True:
            signal = signal_queue.get()
            if signal == "2" and cam2.isOpened():
                print("두번째 카메라 전송")
                ret2, frame2 = cam2.read()
                if ret2:
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

                    result, frame2 = cv2.imencode('.jpg', frame2, encode_param)
                    # frame을 String 형태로 변환
                    data = numpy.array(frame2)
                    stringData = data.tostring()

                    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
        elif signal_queue.empty()  and cam.isOpened():
            ret, frame = cam.read()

            cv2.imshow('', frame)
            if cv2.waitKey(1) == ord('q'):  # q to quit
                raise StopIteration

            if ret:
                ## 0~100에서 90의 이미지 품질로 설정 (default = 95)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

                ## encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
                result, frame = cv2.imencode('.jpg', frame, encode_param)
                # frame을 String 형태로 변환
                data = numpy.array(frame)
                stringData = data.tostring()

                # 서버에 데이터 전송
                s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    cam.release()
    cam2.release()
'''
