-- HiPot Test
HiPotSetup = {
    setup = {v = 500, kelvin = 0, Dwell = 1, tare = {mode = 'fixed', data = {res = 2.5}}},
    criteria = {r_min = 1000},
    diagnose = {scan = 'binary'}
}
IR('Test HiPot', 'hvdc', HiPotSetup, HiPotParameters.Points)
  