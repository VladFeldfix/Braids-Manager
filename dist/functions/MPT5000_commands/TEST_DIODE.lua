-- Test diode
DiodeSetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
Report.Info("Testing diode DIODENAME")
WaitForContinuity('Wait For Continuity', 'Continuity Test: POINT1 to POINT2 for diode DIODENAME. If this message is not disapearing by itself this means that the diode is not working', P1.1, P1.2, 'msr', DiodeSetup, 1)
WaitForNoContinuity('Wait For No Continuity', 'No Continuity Test: POINT2 to POINT1 for diode DIODENAME. If this message is not disapearing by itself this means that the diode is not working', P1.2, P1.1, 'msr', DiodeSetup, 1)