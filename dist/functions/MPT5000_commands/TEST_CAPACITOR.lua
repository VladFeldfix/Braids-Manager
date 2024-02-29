-- Test Capacitor
Capacitor(
  {
    label = 'Test Capacitor CAPNAME',
    device = 'msr',
    setup = {i = 1mA, tare = {mode = 'fixed', data = {res = 2.5}},
    criteria = {c > MINuF, c < MAXuF},
    terminals = {test = POINT1, com = POINT2}
  }
)