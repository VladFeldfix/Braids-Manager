-- Isolation Test
IsolationSetup = {
  setup = {i = 0.1, v = 5, kelvin = 0, tare = {mode = 'fixed', data = {res = 2.5}}},
  criteria = {r_min = 100},
  diagnose = {scan = 'binary'},
}
Isolation('Test Isolation', 'msr', IsolationSetup, 'all')