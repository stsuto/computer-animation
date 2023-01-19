import math
import time

from pyglet.gl import *
import numpy as np

w_height = 600
w_width = 600
config = Config(sample_buffers=1, samples=8)
window = pyglet.window.Window(w_width, w_height, config=config)

tot = 0
os = []
s = [0.0, 0.0, 1.0]
e = [0.0, 0.0, 0.0]


def parse_input_file(file_name):
    with open(file_name, 'r', encoding="utf8") as file:
        V = []
        F = []
        for line in map(str.strip, file.readlines()):
            if not line or (line[0:2] != "v " and line[0:2] != "f "):
                continue
            ident, first, second, third = line.split()
            if ident == 'v':
                V.append((float(first), float(second), float(third)))
            elif ident == 'f':
                F.append((int(first), int(second), int(third)))

        return V, F


def parse_bspline_file(file_name):
    with open(file_name, 'r', encoding="utf8") as file:
        return [np.array(tuple(map(float, line.split())))
                for line in file.readlines()
                if line.strip() and line.strip()[0] != '#']


if __name__ == '__main__':
    v_inp, f = parse_input_file("objects/avion.obj")

    v_count = len(v_inp)

    center = tuple(map(lambda s: s / v_count, map(sum, zip(*v_inp))))
    # center_x, center_y, center_z = map(lambda s: s / v_count, map(sum, zip(*v)))

    mins = tuple(map(min, zip(*v_inp)))
    maxs = tuple(map(max, zip(*v_inp)))

    S = ((maxs[0] + mins[0]) / 2, (maxs[1] + mins[1]) / 2, (maxs[2] + mins[2]) / 2)

    M = max(maxs[0] - mins[0], maxs[1] - mins[1], maxs[2] - mins[2])
    # print(M)

    v = []

    for i in range(0, len(v_inp)):
        v.append(((v_inp[i][0] - S[0]) * 10 / M, (v_inp[i][1] - S[1]) * 10 / M, (v_inp[i][2] - S[2]) * 10 / M))

    v_b = parse_bspline_file("bspline.txt")

    segment_count = len(v_b) - 3

    b = []
    b_print = []
    tan_b_all = []
    tan_b = []

    for i in range(segment_count):
        v0 = v_b[i]
        v1 = v_b[i+1]
        v2 = v_b[i+2]
        v3 = v_b[i+3]

        t_list = (t / 10 for t in range(10))
        # t_list = (t/100 for t in range(100))

        for t_cnt, t in enumerate(t_list):
            f1 = (- pow(t, 3) + 3 * pow(t, 2) - 3 * t + 1) / 6
            f2 = (3 * pow(t, 3) - 6 * pow(t, 2) + 4) / 6
            f3 = (- 3 * pow(t, 3) + 3 * pow(t, 2) + 3 * t + 1) / 6
            f4 = pow(t, 3) / 6

            p = tuple(map(sum, zip(*(f1 * v0, f2 * v1, f3 * v2, f4 * v3))))

            b.append(p)

            t1 = 0.5 * (-pow(t, 2) + 2 * t - 1)
            t2 = 0.5 * (3 * pow(t, 2) - 4 * t)
            t3 = 0.5 * (-3 * pow(t, 2) + 2 * t + 1)
            t4 = 0.5 * (pow(t, 2))

            point2 = tuple(map(sum, zip(*(t1 * v0, t2 * v1, t3 * v2, t4 * v3))))
            point3 = (point2[0], point2[1], point2[2])

            tan_b_all.append(point3)

            b_print.append(p)
            tan_b.append(point3)

            # if t_cnt % 10 == 0:
            #     b_print.append(p)
            #     tan_b.append(point3)


@window.event
def on_draw():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 600 / 400, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1.0, 0.0, 1.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glEnd()


def display():
    global e, os, tot, s

    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glTranslatef(0.0, 0.0, -100.0)
    glRotatef(50, 1, 15, 10)
    glColor3f(0.5, 0, 0)

    glBegin(GL_LINE_STRIP)
    for bb in b:
        glVertex3f(bb[0], bb[1], bb[2])
    glEnd()
    glBegin(GL_LINES)

    for k in range(len(b_print)):
        start = b_print[k]
        end = (tan_b[k][0] + start[0], tan_b[k][1] + start[1], tan_b[k][2] + start[2])
        glVertex3f(*start)
        glVertex3f(*end)
    glEnd()

    glTranslatef(b[tot][0], b[tot][1], b[tot][2])

    # e = (tan_b_all[tot + 1][0] - tan_b_all[tot][0], tan_b_all[tot + 1][1] - tan_b_all[tot][1],
    #      tan_b_all[tot + 1][2] - tan_b_all[tot][2])
    e = tan_b_all[tot]
    os = (s[1] * e[2] - e[1] * s[2], e[0] * s[2] - s[0] * e[1], s[0] * e[1] - s[1] * e[0])

    apsS = pow(pow(s[0], 2) + pow(s[1], 2) + pow(s[2], 2), 0.5)
    apsE = pow(pow(e[0], 2) + pow(e[1], 2) + pow(e[2], 2), 0.5)
    se = s[0] * e[0] + s[1] * e[1] + s[2] * e[2]
    kut = math.acos(se / (apsS * apsE)) * 180

    glRotatef(kut, os[0], os[1], os[2])

    # s = s + np.array(e)
    # print(s)
    s = np.array(e)


    glBegin(GL_LINES)
    for p1, p2, p3 in f:
        v1 = v[p1 - 1]
        v2 = v[p2 - 1]
        v3 = v[p3 - 1]

        glVertex3f(*v1)
        glVertex3f(*v2)

        glVertex3f(*v2)
        glVertex3f(*v3)

        glVertex3f(*v3)
        glVertex3f(*v1)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(*center)
    glVertex3f(center[0] + 2.5, center[1], center[2])

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(*center)
    glVertex3f(center[0], center[1] + 2.5, center[2])

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(*center)
    glVertex3f(center[0], center[1], center[2] + 2.5)

    glColor3f(0.0, 0.0, 0.0)
    glEnd()

    time.sleep(0.1)
    tot += 1
    if tot == len(b) - 1:
        tot = 0

    glFlush()


def animation(args, kwargs):
    display()


pyglet.clock.schedule(animation, 1 / 1000000.0)
pyglet.app.run()
