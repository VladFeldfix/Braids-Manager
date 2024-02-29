-- Point to point test
PointToPointSetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForContinuity("Wait for continuity", "Contact Point: PROBE to Point: POINT1", PROBE, POINT2, 'msr', PointToPointSetup, 1)
Beep(100)
