# -*- coding: utf-8 -*-
'''
IGCProcessor.py

Copyright (c) 2016 Hiraku Toida

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
'''

'''
Class for processing *.igc file
'''

import numpy as np
import datetime

class Record():
    def __init__(self):
        self.payload = []
    def append(self, dat):
        self.payload.append(dat)
    def print_payload(self):
        for line in self.payload:
            print(line[1:-1])

class RecordA(Record):
    def __init__(self):
        super(RecordA, self).__init__()

class RecordB(Record):
    def __init__(self):
        super(RecordB, self).__init__()
        self.dat = []
        self.time = []
        self.gps_valid = []
    def line2dat(self):
        lines = self.payload
        self.dat = np.zeros([len(lines), 10])
        for i, line in enumerate(lines):
            self.dat[i,0] = line[1:7]  # time
            # latitude
            if line[14:15] == 'N':
                latitude_sign = 1
            else:
                latitude_sign = -1
            self.dat[i,1] = latitude_sign * (int(line[7:9]) + int(line[9:14]) / 1000 / 60)
            # longitude
            if line[23:24] == 'E':
                longitude_sign = 1
            else:
                longitude_sign = -1
            self.dat[i,2] = longitude_sign * (int(line[15:18]) + int(line[18:23]) / 1000 / 60)
            # if GPS is avarable or not
            if line[24:25] == 'A':
                self.dat[i,3] = 1
            elif line[24:25] == 'V':
                self.dat[i,3] = 0
            # altitude (pressure)
            self.dat[i,4] = line[25:30]
            # altitude (GPS)
            self.dat[i,5] = line[30:35]
            # FXA
            self.dat[i,6] = line[35:38]
            # ENL
            self.dat[i,7] = line[38:41]
            # GSP
            self.dat[i,8] = line[41:46]
            # TRT
            self.dat[i,9] = line[46:49]
        # time
        for i, _ in enumerate(self.dat):
            if self.dat[i, 3] == 1:
                self.time.append(datetime.datetime.strptime(str(int(self.dat[i,0])), "%H%M%S"))
        self.gps_valid = np.where(self.dat[:,3] == 1)
        self.gps_valid = self.gps_valid[0]

class RecordE(Record):
    def __init__(self):
        super(RecordE, self).__init__()

class RecordF(Record):
    def __init__(self):
        super(RecordF, self).__init__()
        self.dat = []
        self.time = []
    def line2dat(self, date = "010100"):
        lines = self.payload
        self.dat = np.zeros([len(lines), 33])
        for i, line in enumerate(lines):
            self.dat[i,0] = line[1:7]
            for j in range(int((len(line) - 7) / 2)):
                prn = int(line[7+2*j:9+2*j])
                if 0 <= prn and prn <= 32:
                    self.dat[i,prn] = 1

        for i, _ in enumerate(self.dat):
            self.time.append(datetime.datetime.strptime(str(int(self.dat[i,0])), "%H%M%S"))

class RecordG(Record):
    def __init__(self):
        super(RecordG, self).__init__()

class RecordH(Record):
    def __init__(self):
        super(RecordH, self).__init__()
        self.date = ""
    def print_payload(self):
        for line in self.payload:
            if line[1] == 'F':
                print('FR:' + line[2:5] + ' ' + line[5:-1])
    def get_date(self):
        for line in self.payload:
            if line[1:5] == 'FDTE':
                self.date = line[5:11]

class RecordI(Record):
    def __init__(self):
        super(RecordI, self).__init__()
    def print_payload(self):
        for line in self.payload:
            for i in range(int(line[1:3])):
                print(line[7+i*7:10+i*7] + ': ' + line[3+i*7:5+i*7] + ' - ' + line[5+i*7:7+i*7])

class RecordL(Record):
    def __init__(self):
        super(RecordL, self).__init__()
    def print_payload(self):
        for line in self.payload:
            print(line[1:4] + ' ' + line[4:-1])

class IGCProcess():
    def __init__(self):
        self.rec_a = RecordA()
        self.rec_b = RecordB()
        self.rec_e = RecordE()
        self.rec_f = RecordF()
        self.rec_g = RecordG()
        self.rec_h = RecordH()
        self.rec_i = RecordI()
        self.rec_l = RecordL()
    def process_lines(self, lines):
        for line in lines:
            header = line[0]
            if header == 'A':
                self.rec_a.append(line)
            elif header == 'B':
                self.rec_b.append(line)
            elif header == 'E':
                self.rec_e.append(line)
            elif header == 'F':
                self.rec_f.append(line)
            elif header == 'G':
                self.rec_g.append(line)
            elif header == 'H':
                self.rec_h.append(line)
            elif header == 'I':
                self.rec_i.append(line)
            elif header == 'L':
                self.rec_l.append(line)
            else:
                print(line)
