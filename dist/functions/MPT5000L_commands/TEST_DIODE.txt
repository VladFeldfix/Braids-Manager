//TEST DIODE TEST_DIODE
PrintLn(CON + DSK,"TEST DIODE TEST_DIODE;")
SetConductor(HC, Pass < 1 Ohm, I = 1000 mA, V = 5 Volts);
Continuity(POINT1, POINT2);
WaitForNoCont(POINT2, POINT1);
If(PASSED){
    PrintLn(CON + DSK,"  Diode TEST_DIODE is in correct direction");
}
If(FAILED){
    PrintLn(CON + DSK,"  * Diode TEST_DIODE is NOT in correct direction");
    Abort();
}