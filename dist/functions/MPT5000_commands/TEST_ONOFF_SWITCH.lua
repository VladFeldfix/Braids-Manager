-- Test ON-OFF switch
seitchSetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForContinuity("Set switch SWNAME to position ON", POINT1, POINT2, 'msr', seitchSetup, 1);
WaitForNoContinuity("Set switch SWNAME to position OFF", POINT1, POINT2, 'msr', seitchSetup, 1);