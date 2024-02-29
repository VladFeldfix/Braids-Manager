//TEST DC-TO-DC CONVERTER
PrintLn (DSK + CON,": TEST DC-TO-DC CONVERTER CONVERTERNAME");
SetPS(V = 3 Volts, I = 0.2 Amps);
PowerOn((P24V),(P24V_RTN));
Delay(300);
SetPS(V = 24 Volts, I = 0.2 Amps);
Delay(300);
SetReadVolts(LV, DC, MIN = 4.9 Volts, MAX = 5.1  Volts);
ReadVolts((P5V),(P5V_RTN));
PowerOff();