//TEST RESISTOR
PrintLn(CON+DSK,"TEST RESNAME [OHM Ohm] - 2 wire");
SetResistance(LV, Pass = OHM Ohms +- 5%, I = Auto);
Resistor(POINT1,POINT2);