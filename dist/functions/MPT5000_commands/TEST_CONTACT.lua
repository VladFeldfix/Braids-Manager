-- Continuity Test 
ContinuitySetup = {
  setup = {i = 0.1, v = 5, Kelvin = 0, tare = {mode = 'fixed', data = {res = 2.5}}},
  criteria = {r_max = 1},
}
Continuity('Continuity Test', 'msr', ContinuitySetup)