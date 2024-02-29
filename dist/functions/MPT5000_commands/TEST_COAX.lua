-- Test coax cable COAXNAME
Report.Info("Test coax cable COAXNAME")
Report.Info("Measuring DATA resistance DATA1 to DATA2 for coax cable COAXNAME")
SetHigh(DATA1)
SetLow(DATA2)
DataRes = DoResistance('msr', {i = 100mA, delay = 100ms, v = 5, tare = {mode = 'fixed', data = {res = 2.5}}})
Report.Info("DATA resistance DATA1 to DATA2 = "..DataRes.value_as_str)
ClearAllPoints()

Report.Info("Measuring BRAID resistance BRAID1 to BRAID2 for coax cable COAXNAME")
SetHigh(BRAID1)
SetLow(BRAID2)
BraidRes = DoResistance('msr', {i = 100mA, delay = 100ms, v = 5, tare = {mode = 'fixed', data = {res = 2.5}}})
Report.Info("BRAID resistance BRAID1 to BRAID2 = "..BraidRes.value_as_str)
ClearAllPoints()

Report.Info("Comparing DATA to BRAID")
if DataRes.value > BraidRes.value then
  Report.Pass('Passed! Signal resistance is greater than braid resistance: '..DataRes.value_as_str.." > "..BraidRes.value_as_str)
else
  Report.Fail('* Failed! Signal resistance is smaller than braid resistance: '..DataRes.value_as_str.." < "..BraidRes.value_as_str)
end