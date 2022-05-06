from datetime import datetime

'''t1 = datetime.datetime(2021, 12, 1, 8, 50)
t2 = datetime.datetime(2021, 12, 1, 10, 20)

delta = t2-t1
print delta.total_seconds()
'''

startrun1 = datetime(2021, 11, 29, 10, 11)
stoprun1 = datetime(2021, 11, 29, 11, 8)
startrun2 = datetime(2021, 11, 29, 11, 9)
stoprun2 = datetime(2021, 11, 29, 11, 59)
startrun3 = datetime(2021, 11, 29, 11, 59)
stoprun3 = datetime(2021, 11, 29, 12, 25)
startrun4 = datetime(2021, 11, 29, 12, 29)
stoprun4 = datetime(2021, 11, 29, 14, 50)
startrun5 = datetime(2021, 11, 29, 16, 55)
stoprun5 = datetime(2021, 11, 29, 17, 7)
startrun6 = datetime(2021, 11, 29, 17, 33)
stoprun6 = datetime(2021, 11, 29, 18, 44)
startrun7 = datetime(2021, 11, 29, 18, 49)
stoprun7 = datetime(2021, 11, 29, 19, 5)
startrun8 = datetime(2021, 11, 30, 9, 30)
stoprun8 =  datetime(2021, 11, 30, 9, 44)
startrun9 = datetime(2021, 11, 30, 10, 19)
stoprun9 = datetime(2021, 11, 30, 10, 47)
startrun10 = datetime(2021, 11, 30, 10, 50)
stoprun10 = datetime(2021, 11, 30, 14, 4)
startrun11 = datetime(2021, 11, 30, 14, 31)
stoprun11 = datetime(2021, 11, 30, 15, 35)
startrun12 = datetime(2021, 11, 30, 15, 37)
stoprun12 = datetime(2021, 11, 30, 16, 55)
startrun13 = datetime(2021, 11, 30, 16, 55)
stoprun13 = datetime(2021, 11, 30, 17, 50)
startrun14 = datetime(2021, 11, 30, 18, 17)
stoprun14 = datetime(2021, 11, 30, 19, 11)
startrun15 = datetime(2021, 11, 30, 19, 17)
stoprun15 = datetime(2021, 12, 1, 8, 20)
startrun16 = datetime(2021, 12, 1, 8, 53)
stoprun16 = datetime(2021, 12, 1, 9, 21)
startrun17 = datetime(2021, 12, 1, 9, 35)
stoprun17 = datetime(2021, 12, 1, 10, 22)
startrun18 = datetime(2021, 12, 1, 10, 23)
stoprun18 = datetime(2021, 12, 1, 10, 39)
startrun19 = datetime(2021, 12, 1, 10, 40)
stoprun19 = datetime(2021, 12, 1, 11, 46)
startrun20 = datetime(2021, 12, 1, 12, 56)
stoprun20 = datetime(2021, 12, 1, 14, 24)
startrun21 = datetime(2021, 12, 1, 15, 23)
stoprun21 = datetime(2021, 12, 1, 16, 44)
startrun22 = datetime(2021, 12, 1, 17, 26)
stoprun22 = datetime(2021, 12, 1, 18, 47)
startrun23 = datetime(2021, 12, 2, 9, 26)
stoprun23 = datetime(2021, 12, 2, 12, 27)
startrun24 = datetime(2021, 12, 2, 12, 27)
stoprun24 = datetime(2021, 12, 2, 16, 9)
startrun25 = datetime(2021, 12, 2, 16, 10)
stoprun25 = datetime(2021, 12, 2, 18, 31)
startrun26 = datetime(2021, 12, 2, 18, 43)
stoprun26 = datetime(2021, 12, 2, 19, 11)
startrun27 = datetime(2021, 12, 2, 19, 12)
stoprun27 = datetime(2021, 12, 3, 9, 7)
startrun28 = datetime(2021, 12, 3, 10, 29)
stoprun28 = datetime(2021, 12, 3, 11, 51)
startrun29 = datetime(2021, 12, 3, 12, 10)
stoprun29 = datetime(2021, 12, 3, 13, 18)
startrun30 = datetime(2021, 12, 3, 13, 20)
stoprun30 = datetime(2021, 12, 3, 14, 11)
startrun31 = datetime(2021, 12, 3, 14, 22)
stoprun31 = datetime(2021, 12, 3, 17, 7)
startrun32 = datetime(2021, 12, 3, 17, 11)
stoprun32 = datetime(2021, 12, 4, 11, 9)
startrun33 = datetime(2021, 12, 4, 15, 0)
stoprun33 = datetime(2021, 12, 5, 22, 56)


PICO1 = { 
    "run0001":{"start_time": startrun1,"stop_time": stoprun1,"tot_time": (stoprun1-startrun1).total_seconds() },
    "run0002":{"start_time": startrun2,"stop_time": stoprun2,"tot_time": (stoprun2-startrun2).total_seconds() },
    "run0003":{"start_time": startrun3,"stop_time": stoprun3,"tot_time": (stoprun3-startrun3).total_seconds()},
    "run0004":{"start_time": startrun4,"stop_time": stoprun4,"tot_time": (stoprun4-startrun4).total_seconds()},
    "run0005":{"start_time": startrun5,"stop_time": stoprun5,"tot_time": (stoprun5-startrun5).total_seconds()},
    "run0006":{"start_time": startrun6,"stop_time": stoprun6,"tot_time": (stoprun6-startrun6).total_seconds()},
    "run0007":{"start_time": startrun7,"stop_time": stoprun7,"tot_time": (stoprun7-startrun7).total_seconds()},
    "run0008":{"start_time": startrun8,"stop_time": stoprun8,"tot_time": (stoprun8-startrun8).total_seconds()},
    "run0009":{"start_time": startrun9,"stop_time": stoprun9,"tot_time": (stoprun9-startrun9).total_seconds()},
    "run0010":{"start_time": startrun10,"stop_time": stoprun10,"tot_time": (stoprun10-startrun10).total_seconds()},
    "run0011":{"start_time": startrun11,"stop_time": stoprun11,"tot_time": (stoprun11-startrun11).total_seconds()},
    "run0012":{"start_time": startrun12,"stop_time": stoprun12,"tot_time": (stoprun12-startrun12).total_seconds()},
    "run0013":{"start_time": startrun13,"stop_time": stoprun13,"tot_time": (stoprun13-startrun13).total_seconds()},
    "run0014":{"start_time": startrun14,"stop_time": stoprun14,"tot_time": (stoprun14-startrun14).total_seconds()},
    "run0015":{"start_time": startrun15,"stop_time": stoprun15,"tot_time": (stoprun15-startrun15).total_seconds()},
    "run0016":{"start_time": startrun16,"stop_time": stoprun16,"tot_time": (stoprun16-startrun16).total_seconds()},
    "run0017":{"start_time": startrun17,"stop_time": stoprun17,"tot_time": (stoprun17-startrun17).total_seconds()},
    "run0018":{"start_time": startrun18,"stop_time": stoprun18,"tot_time": (stoprun18-startrun18).total_seconds()},
    "run0019":{"start_time": startrun19,"stop_time": stoprun19,"tot_time": (stoprun19-startrun19).total_seconds()},
    "run0020":{"start_time": startrun20,"stop_time": stoprun20,"tot_time": (stoprun20-startrun20).total_seconds()},
    "run0021":{"start_time": startrun21,"stop_time": stoprun21,"tot_time": (stoprun21-startrun21).total_seconds()},
    "run0022":{"start_time": startrun22,"stop_time": stoprun22,"tot_time": (stoprun22-startrun22).total_seconds()},
    "run0023":{"start_time": startrun23,"stop_time": stoprun23,"tot_time": (stoprun23-startrun23).total_seconds()},
    "run0024":{"start_time": startrun24,"stop_time": stoprun24,"tot_time": (stoprun24-startrun24).total_seconds()},
    "run0025":{"start_time": startrun25,"stop_time": stoprun25,"tot_time": (stoprun25-startrun25).total_seconds()},
    "run0026":{"start_time": startrun26,"stop_time": stoprun26,"tot_time": (stoprun26-startrun26).total_seconds()},
    "run0027":{"start_time": startrun27,"stop_time": stoprun27,"tot_time": (stoprun27-startrun27).total_seconds()},
    "run0028":{"start_time": startrun28,"stop_time": stoprun28,"tot_time": (stoprun28-startrun28).total_seconds()},
    "run0029":{"start_time": startrun29,"stop_time": stoprun29,"tot_time": (stoprun29-startrun29).total_seconds()},
    "run0030":{"start_time": startrun30,"stop_time": stoprun30,"tot_time": (stoprun30-startrun30).total_seconds()},
    "run0031":{"start_time": startrun31,"stop_time": stoprun31,"tot_time": (stoprun31-startrun31).total_seconds()},
    "run0032":{"start_time": startrun32,"stop_time": stoprun32,"tot_time": (stoprun32-startrun32).total_seconds()},
    "run0033":{"start_time": startrun33,"stop_time": stoprun33,"tot_time": (stoprun33-startrun33).total_seconds()}

}

startrun1 = datetime(2021, 11, 29, 10, 10)
stoprun1 = datetime(2021, 11, 29, 11, 8)
startrun2 = datetime(2021, 11, 29, 11, 8)
stoprun2 = datetime(2021, 11, 29, 11, 58)
startrun3 = datetime(2021, 11, 29, 12, 0)
stoprun3 = datetime(2021, 11, 29, 12, 24)
startrun4 = datetime(2021, 11, 29, 12, 29)
stoprun4 = datetime(2021, 11, 29, 14, 50)
startrun5 = datetime(2021, 11, 29, 16, 55)
stoprun5 = datetime(2021, 11, 29, 17, 7)
startrun6 = datetime(2021, 11, 29, 17, 33)
stoprun6 = datetime(2021, 11, 29, 18, 44)
startrun7 = datetime(2021, 11, 29, 18, 49)
stoprun7 = datetime(2021, 11, 29, 19, 5)
startrun8 = datetime(2021, 11, 30, 9, 30)
stoprun8 =  datetime(2021, 11, 30, 9, 44)
startrun9 = datetime(2021, 11, 30, 10, 19)
stoprun9 = datetime(2021, 11, 30, 10, 47)
startrun10 = datetime(2021, 11, 30, 10, 48)
stoprun10 = datetime(2021, 11, 30, 14, 4)
startrun11 = datetime(2021, 11, 30, 15, 38)
stoprun11 = datetime(2021, 11, 30, 16, 55)
startrun12 = datetime(2021, 11, 30, 16, 58)
stoprun12 = datetime(2021, 11, 30, 17, 50)
startrun13 = datetime(2021, 11, 30, 18, 18)
stoprun13 = datetime(2021, 11, 30, 19, 11)
startrun14 = datetime(2021, 11, 30, 19, 17)
stoprun14 = datetime(2021, 12, 1, 8, 20)
startrun15 = datetime(2021, 12, 1, 8, 53)
stoprun15 = datetime(2021, 12, 1, 9, 21)
startrun16 = datetime(2021, 12, 1, 9, 36)
stoprun16 = datetime(2021, 12, 1, 10, 22)
startrun17 = datetime(2021, 12, 1, 10, 24)
stoprun17 = datetime(2021, 12, 1, 10, 39)
startrun18 = datetime(2021, 12, 1, 10, 40)
stoprun18 = datetime(2021, 12, 1, 11, 46)
startrun19 = datetime(2021, 12, 1, 12, 55)
stoprun19 = datetime(2021, 12, 1, 14, 24)
startrun20 = datetime(2021, 12, 1, 15, 24)
stoprun20 = datetime(2021, 12, 1, 16, 44)
startrun21 = datetime(2021, 12, 1, 17, 26)
stoprun21 = datetime(2021, 12, 1, 18, 47)
startrun22 = datetime(2021, 12, 2, 9, 26)
stoprun22 = datetime(2021, 12, 2, 12, 27)
startrun23 = datetime(2021, 12, 2, 12, 28)
stoprun23 = datetime(2021, 12, 2, 16, 9)
startrun24 = datetime(2021, 12, 2, 16, 9)
stoprun24 = datetime(2021, 12, 2, 18, 31)
startrun25 = datetime(2021, 12, 2, 18, 43)
stoprun25 = datetime(2021, 12, 2, 19, 11)
startrun26 = datetime(2021, 12, 2, 19, 12)
stoprun26 = datetime(2021, 12, 3, 9, 6)
startrun27 = datetime(2021, 12, 3, 10, 29)
stoprun27 = datetime(2021, 12, 3, 11, 51)
startrun28 = datetime(2021, 12, 3, 12, 10)
stoprun28 = datetime(2021, 12, 3, 13, 10)
startrun29 = datetime(2021, 12, 3, 13, 20)
stoprun29 = datetime(2021, 12, 3, 14, 11)
startrun30 = datetime(2021, 12, 3, 14, 22)
stoprun30 = datetime(2021, 12, 3, 17, 7)
startrun31 = datetime(2021, 12, 3, 17, 11)
stoprun31 = datetime(2021, 12, 4, 11, 9)
startrun32 = datetime(2021, 12, 5, 15, 0)
stoprun32 = datetime(2021, 12, 5, 22, 56)

PICO2 = { 
    "run0001":{"start_time": startrun1,"stop_time": stoprun1,"tot_time": (stoprun1-startrun1).total_seconds()},
    "run0002":{"start_time": startrun2,"stop_time": stoprun2,"tot_time": (stoprun2-startrun2).total_seconds()},
    "run0003":{"start_time": startrun3,"stop_time": stoprun3,"tot_time": (stoprun3-startrun3).total_seconds()},
    "run0004":{"start_time": startrun4,"stop_time": stoprun4,"tot_time": (stoprun4-startrun4).total_seconds()},
    "run0005":{"start_time": startrun5,"stop_time": stoprun5,"tot_time": (stoprun5-startrun5).total_seconds()},
    "run0006":{"start_time": startrun6,"stop_time": stoprun6,"tot_time": (stoprun6-startrun6).total_seconds()},
    "run0007":{"start_time": startrun7,"stop_time": stoprun7,"tot_time": (stoprun7-startrun7).total_seconds()},
    "run0008":{"start_time": startrun8,"stop_time": stoprun8,"tot_time": (stoprun8-startrun8).total_seconds()},
    "run0009":{"start_time": startrun9,"stop_time": stoprun9,"tot_time": (stoprun9-startrun9).total_seconds()},
    "run0010":{"start_time": startrun10,"stop_time": stoprun10,"tot_time": (stoprun10-startrun10).total_seconds()},
    "run0011":{"start_time": startrun11,"stop_time": stoprun11,"tot_time": (stoprun11-startrun11).total_seconds()},
    "run0012":{"start_time": startrun12,"stop_time": stoprun12,"tot_time": (stoprun12-startrun12).total_seconds()},
    "run0013":{"start_time": startrun13,"stop_time": stoprun13,"tot_time": (stoprun13-startrun13).total_seconds()},
    "run0014":{"start_time": startrun14,"stop_time": stoprun14,"tot_time": (stoprun14-startrun14).total_seconds()},
    "run0015":{"start_time": startrun15,"stop_time": stoprun15,"tot_time": (stoprun15-startrun15).total_seconds()},
    "run0016":{"start_time": startrun16,"stop_time": stoprun16,"tot_time": (stoprun16-startrun16).total_seconds()},
    "run0017":{"start_time": startrun17,"stop_time": stoprun17,"tot_time": (stoprun17-startrun17).total_seconds()},
    "run0018":{"start_time": startrun18,"stop_time": stoprun18,"tot_time": (stoprun18-startrun18).total_seconds()},
    "run0019":{"start_time": startrun19,"stop_time": stoprun19,"tot_time": (stoprun19-startrun19).total_seconds()},
    "run0020":{"start_time": startrun20,"stop_time": stoprun20,"tot_time": (stoprun20-startrun20).total_seconds()},
    "run0021":{"start_time": startrun21,"stop_time": stoprun21,"tot_time": (stoprun21-startrun21).total_seconds()},
    "run0022":{"start_time": startrun22,"stop_time": stoprun22,"tot_time": (stoprun22-startrun22).total_seconds()},
    "run0023":{"start_time": startrun23,"stop_time": stoprun23,"tot_time": (stoprun23-startrun23).total_seconds()},
    "run0024":{"start_time": startrun24,"stop_time": stoprun24,"tot_time": (stoprun24-startrun24).total_seconds()},
    "run0025":{"start_time": startrun25,"stop_time": stoprun25,"tot_time": (stoprun25-startrun25).total_seconds()},
    "run0026":{"start_time": startrun26,"stop_time": stoprun26,"tot_time": (stoprun26-startrun26).total_seconds()},
    "run0027":{"start_time": startrun27,"stop_time": stoprun27,"tot_time": (stoprun27-startrun27).total_seconds()},
    "run0028":{"start_time": startrun28,"stop_time": stoprun28,"tot_time": (stoprun28-startrun28).total_seconds()},
    "run0029":{"start_time": startrun29,"stop_time": stoprun29,"tot_time": (stoprun29-startrun29).total_seconds()},
    "run0030":{"start_time": startrun30,"stop_time": stoprun30,"tot_time": (stoprun30-startrun30).total_seconds()},
    "run0031":{"start_time": startrun31,"stop_time": stoprun31,"tot_time": (stoprun31-startrun31).total_seconds()},
    "run0032":{"start_time": startrun32,"stop_time": stoprun32,"tot_time": (stoprun32-startrun32).total_seconds()}
}

dict_run = {"PICO1":PICO1, "PICO2":PICO2}


#print startrun30
