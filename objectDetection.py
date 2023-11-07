import cv2

thres = 0.45  # Threshold to detect object

# def __init__():

classNames = []
classFile = 'res/coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'res/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'res/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def detect_object(img):
    """ the output contains a list of tuples
    Each tuple has 3 values
    1. Object name
    2. Accuracy
    3. Image with bounding rectangle, name, accuracy """

    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    # print(classIds,bbox)
    # print(confs)
    res = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            # cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            # cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
            #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            # cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
            #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            res.append((classNames[classId - 1], round(confidence * 100, 2), img))
    return res


# for t in detect_object(cv2.imread(test_img)):
#     print(t[:2])
#     cv2.imshow("img",t[2])
#
# cv2.waitKey(0)
