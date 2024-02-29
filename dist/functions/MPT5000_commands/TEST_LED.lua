-- Test LED
SetHighAuxiliary(POINT1)
SetLowAuxiliary(POINT2)
SetPPSOn('hcs', {i = 0.01, v = 28})
Sleep(1)
LED = ConfirmationPrompt ('Confirm that LEDNAME is COLOR', 'LED Test')
if not LED then Report.Fail('* LED LEDNAME Failed') else Report.Pass('LED LEDNAME Passed') end
SetPPSOff('hcs')
ClearAllPoints()