-- Test ON-OFF switch
seitchSetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForContinuity('Wait For Continuity', "Set switch SWNAME to position POSITION", POINT1, POINT2, 'msr', seitchSetup, 1);