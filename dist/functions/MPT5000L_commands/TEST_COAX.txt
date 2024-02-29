//TEST COAX CABLE
PrintLn (DSK + CON,": TEST COAX CABLE COAXNAME");
Lua(
    -- Test Signal
    ClrAllTest(false)
    ClrAllCom(false)
    SetTest(false,"DATA1")
    SetCom(false,"DATA2")
    printtodevices(DSK + CON, " Measure signal resistance DATA1 - DATA2")
    DoContinuity()
    signal_resistance = lastresmeasurement

    -- Test braid
    ClrAllTest(false)
    ClrAllCom(false)
    SetTest(false,"BRAID1")
    SetCom(false,"BRAID2")
    printtodevices(DSK + CON, " Measure braid resistance BRAID1 - BRAID2")
    DoContinuity()
    braid_resistance = lastresmeasurement

    -- Compare
    if signal_resistance > braid_resistance then
        printtodevices(DSK + CON, " Test Result: Signal Res > Braid Res", signal_resistance, " > " ,braid_resistance)
        printtodevices(DSK + CON, " PASS")
    else
        printtodevices(DSK + CON, "* FAIL")
        printtodevices(DSK + CON, " Check COAXNAME COAX cable wiring")
        AbortTest()
    end
    printtodevices(DSK + CON, "")
)