-- Test relay
SetHighAuxiliary(INPUT_PLUS)
SetLowAuxiliary(INPUT_MINUS)
SetPPSOn('hcs', {i = 0.02, v = 24})
Sleep(300)
RelaySetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForContinuity("Wait for continuity", "Testing relay RELAYNAME", OUTPUT_PLUS, OUTPUT_MINUS, 'msr', RelaySetup, 1)
ClearAllPoints()
SetPPSOff('hcs')