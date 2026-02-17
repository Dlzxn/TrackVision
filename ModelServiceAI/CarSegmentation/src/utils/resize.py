


def resize_frame(frame, param):
    x1, y1, x2, y2 = param
    return frame[y1:y2, x1:x2]