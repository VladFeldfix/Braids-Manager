# GENERAL INFORMATION
## The purpose of this application is to maintain a database of all the testing cables
## Follow document ELECTRICAL TESTING PROCEDURE to see usage instructions

# HOW TO USE
## Download the application
## Set all the settings according to PART V
## Run App_Name.exe file

from PersonalAssistant import *
from PersonalAssistant import FIELD
import os
import sqlite3

class main:
    def __init__(self):
        # set up Personal Assistant
        self.pa = PersonalAssistant(__file__, "Braids Manager", "2.0")
        
        # connect to database
        self.db_location = self.pa.get_setting("Database location")
        self.con = sqlite3.connect(self.db_location)
        self.cur = self.con.cursor()

        # create database tables
        self.cur.execute("CREATE TABLE IF NOT EXISTS BRAIDS (TEST_CABLE_ID INT, BRAID_ID VARCHAR(10), PLUG_PART_NUMBER VARCHAR(50), PLUG_FLEX_PART_NUMBER VARCHAR(50), SIZE INT, PIN_TYPE VARCHAR(10))")
        self.con.commit()

        # global variables
        self.pin_types = ("PIN", "SOCKET", "BOTH")

        # make sure that all files exist
        self.braids_location = self.pa.get_setting("Braids Location")
        self.lbl_location = self.pa.get_setting("Labels Location")
        self.lbl_locations = (self.braids_location, self.lbl_location, self.lbl_location+"/LBL MPT AR00179 Storage Box.btw", self.lbl_location+"/LBL MPT AR00179 Hood Number.btw", self.lbl_location+"/LBL MPT AR00179 Hood ABC.btw", self.lbl_location+"/LBL MPT AR00179 Test Cable Number.btw", self.lbl_location+"/LBL MPT AR00179 Braid Number.btw", self.lbl_location+"/LBL MPT AR00179 Plastic Bag Label.btw")
        for path in self.lbl_locations:
            if (not os.path.isdir(path)) and (not os.path.isfile(path)):
                self.pa.fatal_error("Missing: "+path)
        
        # display database
        self.update_database()
        self.display_database()

        # MAIN MENU
        self.pa.main_menu["ADD NEW TEST CABLE"] = self.add
        self.pa.display_menu()

        # run GUI
        self.pa.run()

    def display_database(self):
        self.pa.display_database(self.db_location, "BRAIDS", "TEST_CABLE_ID")

    def restart(self):
        # update database
        self.update_database()

        # display database
        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()
    
    def update_database(self):
        # update database
        self.cur.execute("DELETE FROM BRAIDS")
        for root, dirs, files in os.walk(self.braids_location):
            for file in files:
                if ".csv" in file:
                    # read the map
                    mapfile = self.pa.read_csv(root+"/"+file)
                    braids_sizes = {}
                    braids_plugs = {}
                    used_pins = {}
                    for line in mapfile[1:]:
                        if len(line) >= 3:
                            if line[1] != "":
                                if not line[1] in braids_sizes:
                                    if line[2] != "BODY":
                                        if not line[2] in used_pins:
                                            used_pins[line[2]] = 1
                                            braids_sizes[line[1]] = 1
                                else:
                                    if line[2] != "BODY":
                                        if not line[2] in used_pins:
                                            used_pins[line[2]] = 1
                                            braids_sizes[line[1]] += 1
                        if len(line) >= 6:
                            if not line[3] in braids_plugs and line[3] != "":
                                braids_plugs[line[3]] = [line[4], line[5], line[6]]
                    for braid_id, size in braids_sizes.items():
                        if braid_id in braids_plugs:
                            if len(braids_plugs[braid_id]) == 3:
                                braids_plugs[braid_id].append(size)
                    
                    # write map details to database
                    TEST_CABLE_ID = file.replace(".csv", "")
                    for braid_id, value in braids_plugs.items():
                        BRAID_ID = braid_id
                        PLUG_PART_NUMBER = value[0]
                        PLUG_FLEX_PART_NUMBER = value[1]
                        PIN_TYPE = value[2]
                        if len(value) == 4:
                            SIZE = value[3]
                        else:
                            SIZE = 0
                        self.cur.execute("INSERT INTO BRAIDS (TEST_CABLE_ID, BRAID_ID, PLUG_PART_NUMBER, PLUG_FLEX_PART_NUMBER, SIZE, PIN_TYPE) VALUES ("+str(TEST_CABLE_ID)+",'"+str(TEST_CABLE_ID)+"."+str(BRAID_ID)+"','"+PLUG_PART_NUMBER+"','"+PLUG_FLEX_PART_NUMBER+"',"+str(SIZE)+",'"+PIN_TYPE+"')")
        
        # commit changes
        self.con.commit()

    def add(self):
        ## ADD NEW TEST CABLE
        self.pa.print("Adding a new test cable")

        # get test cable information
        error = True
        
        # get test cable ID
        test_cable_id = 1
        self.cur.execute("SELECT * FROM BRAIDS ORDER BY TEST_CABLE_ID")
        fetched_values = self.cur.fetchall()
        if len(fetched_values) != 0:
            test_cable_id = fetched_values[-1][0] + 1

        # barid id
        braid_id = 1

        # global points
        self.pa.print("TEST CABLE #"+str(test_cable_id))
        global_points = self.pa.input("How many MPT plugs the new test cable has? [Leave empty for default value of 1]") or 1
        try:
            global_points = int(global_points)
        except:
            global_points = 1
        
        # braids
        qty = self.pa.input("How many braids the new test cable has? [Leave empty for default value of 1]") or 1
        try:
            qty = int(qty)
        except:
            qty = 1
        
        # for each braid
        braids = []
        while braid_id <= qty:
            plug_pn = self.pa.input("Insert PART NUMBER for plug #"+str(test_cable_id)+"."+str(braid_id)+" [Leave empty for default value NONE]") or "NONE"
            flex_pn = self.pa.input("Insert FLEX PART NUMBER for plug #"+str(test_cable_id)+"."+str(braid_id)+" [Leave empty for default value NONE]") or "NONE"
            pin_type = self.pa.choose("Insert PIN TYPE for plug #"+str(test_cable_id)+"."+str(braid_id)+" [Leave empty for default value BOTH]", self.pin_types, self.pin_types[2])
            braids.append((plug_pn, flex_pn, pin_type))
            braid_id += 1
        
        # open labels
        for path in self.lbl_locations[2:]:
            os.popen(path)
        self.pa.input("Finish printing and placing all the labels then click ENTER to continue")

        # open map
        file = open(self.braids_location+"/"+str(test_cable_id)+".csv", "w")
        for line in range((global_points*50)+1):
            if line == 0:
                file.write("GLOBAL_POINT,BRAID_ID,PIN,BRIAD,PLUG_PART_NUMBER,FLEX_PLUG_PART_NUMBER,PIN_TYPE\n")
            elif line > 0:
                if line <= len(braids):
                    file.write(str(line)+",,,"+str(line)+","+braids[line-1][0]+","+braids[line-1][1]+","+braids[line-1][2]+"\n")
                else:
                    file.write(str(line)+"\n")
        file.close()
        os.popen(self.braids_location+"/"+str(test_cable_id)+".csv")
        self.pa.input("Finish editing the map, then click ENTER to continue")

        # restart
        self.restart()
main()

# SCRIPT FUNCTIONS

# SETTINGS
# Database location --> The location of the user database. For example: database.db

# RELATED FILES