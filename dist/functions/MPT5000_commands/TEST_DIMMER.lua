-- Test dimmer
Report.Info("Testing dimmer DIMNAME")
InfoMessageBox('Set dimmer DIMNAME max clockwise and press Continue','Dimmer Test')
Resistor(
  {
    label='Testing Resistance POINT3 to POINT2 for dimmer DIMNAME max clockwise',
    device='msr',
    setup = {i = 0.1, Kelvin = 0, tare = {mode = 'fixed', data = {res = 2.5}}},
    criteria = {r = MAXOHMΩ ± 5%},
    terminals = {test = POINT3, com = POINT2}
  }
)
ContinuitySetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForContinuity("Wait for continuity", "Contact Point: PROBE to Point: POINT1", POINT3, POINT1, 'msr', ContinuitySetup, MINOHM)

InfoMessageBox('Set dimmer DIMNAME max counter-clockwise and press Continue','Dimmer Test')
Resistor(
  {
    label='Testing Resistance POINT3 to POINT2 for dimmer DIMNAME max counter-clockwise',
    device='msr',
    setup = {i = 0.1, Kelvin = 0, tare = {mode = 'fixed', data = {res = 2.5}}},
    criteria = {r = MAXOHMΩ ± 5%},
    terminals = {test = POINT3, com = POINT1}
  }
)
ContinuitySetup = {i = 0.1, tare = {mode = 'fixed', data = {res = 2.5}}}
WaitForContinuity("Wait for continuity", "Contact Point: PROBE to Point: POINT1", POINT3, POINT2, 'msr', ContinuitySetup, MINOHM)

InfoMessageBox("Set dimmer DIMNAME to neutral position")
WaitForNoContinuity(POINT3, POINT1)
WaitForNoContinuity(POINT3, POINT2)