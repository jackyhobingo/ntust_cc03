
import math

def get_d(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)** 2 + (y1 - y2)** 2)

def get_area(x1,y1,x2,y2,r1,r2):
    # todo : 修正公式
    d = get_d(x1, y1, x2, y2)
    if d < r2:
        return r1 * r1 * math.pi
    r = r1*r1*math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    R = r2*r2*math.acos((d**2 - r1**2 + r2**2) / (2 * d * r2))
    tri = 0.5*math.sqrt((-d + r1 + r2) * (d + r1 - r2 )*(d - r1 + r2)*(d + r1 + r2))
    return r + R - tri


def list_add(list1: list, list2: list):

    ans = []
    for x, y in zip(list1, list2):
        ans.append(x + y)
    return ans