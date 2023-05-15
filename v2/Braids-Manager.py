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

        """
        ## ADD
        #- This will allow you to add a new test cables to the database by filling a form
        #- At the end of the form press Y to submit the form and the new test cables will be added to the database

        # get test cable ID
        test_cable_id = 1
        self.cur.execute("SELECT * FROM braids")
        fetched_values = self.cur.fetchall()
        if len(fetched_values) != 0:
            test_cable_id = fetched_values[-1][0] + 1
        
        # get braids qty
        qty = self.pa.input("Test cable #"+str(test_cable_id)+"\nHow many braids this test cable has? [Leave empty for default value 1]") or 1
        try:
            qty = int(qty)
        except:
            qty = 1
        
        # fill form for every braid
        continue_adding = True
        for i in range(1,qty+1):
            if continue_adding:
                fields = {}
                fields["TEST CABLE ID"] = FIELD("TEST CABLE ID", NUMBER, test_cable_id)
                fields["TEST CABLE ID"].disabled = True
                fields["BRAID ID"] = FIELD("BRAID ID", NUMBER, i)
                fields["BRAID ID"].disabled = True
                fields["CUSTOMER PART NUMBER"] = FIELD("CUSTOMER PART NUMBER", TEXT, "NONE")
                fields["FLEX PART NUMBER"] = FIELD("FLEX PART NUMBER", TEXT, "NONE")
                fields["SIZE"] = FIELD("SIZE", NUMBER, 10)
                fields["PIN TYPE"] = FIELD("PIN TYPE", CHOOSE, self.pin_types[0])
                fields["PIN TYPE"].options = self.pin_types
                braid_id = str(test_cable_id)+"."+str(i)
                
                # submit form and update database
                submit = self.pa.form(fields)
                if submit:
                    self.cur.execute("INSERT INTO braids (test_cable_id, braid_id, customer_pn, flex_pn, size, ps) VALUES ("+str(submit["TEST CABLE ID"])+","+str(submit["BRAID ID"])+",'"+str(submit["CUSTOMER PART NUMBER"])+"','"+str(submit["FLEX PART NUMBER"])+"',"+str(submit["SIZE"])+",'"+str(submit["PIN TYPE"])+"')")
                    self.con.commit()
                    self.pa.print("Briad #: "+braid_id+" added successfully!")
                else:
                    self.pa.error("New braid was NOT added to the database")
                    continue_adding = False
        
        # restart
        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()

    def edit(self):
        ## EDIT
        #- This will allow you to edit an existing test cable by filling a form
        #- At the end of the form press Y to submit the form and the test cable information will be edited
        
        # get test cable id to edit
        ans = self.pa.input("What braid would you like to edit? [Insert in the following format: test_cable_id.braid_id (For example: 12.4)]")
        ans = ans.split(".")
        error = False
        if len(ans) != 2:
            self.pa.error("Error! Invalid input")
            error = True
        else:
            test_cable_id = ans[0]
            braid_id = ans[1]
        
        # check if test cable exists
        if not error:
            self.cur.execute("SELECT * FROM braids WHERE test_cable_id = "+test_cable_id)
            fetched_values = self.cur.fetchall()
            if len(fetched_values) == 0:
                error = True
                self.pa.error("Test cable: "+test_cable_id+" is not in the database")
        
        # check if braid exists
        if not error:
            self.cur.execute("SELECT * FROM braids WHERE braid_id = "+braid_id)
            fetched_values = self.cur.fetchall()
            if len(fetched_values) == 0:
                error = True
                self.pa.error("Braid: "+braid_id+" in test cable: "+test_cable_id+" is not in the database")
        
        # get default values
        if not error:
            data = fetched_values[0]
            test_cable_id = data[0]
            braid_id = data[1]
            customer_pn = data[2]
            flex_pn = data[3]
            size = data[4]
            ps = data[5]

            # set up form
            fields = {}
            fields["TEST CABLE ID"] = FIELD("TEST CABLE ID", NUMBER, test_cable_id)
            fields["TEST CABLE ID"].disabled = True
            fields["BRAID ID"] = FIELD("BRAID ID", NUMBER, braid_id)
            fields["BRAID ID"].disabled = True
            fields["CUSTOMER PART NUMBER"] = FIELD("CUSTOMER PART NUMBER", TEXT, customer_pn)
            fields["FLEX PART NUMBER"] = FIELD("FLEX PART NUMBER", TEXT, flex_pn)
            fields["SIZE"] = FIELD("SIZE", NUMBER, size)
            fields["PIN TYPE"] = FIELD("PIN TYPE", CHOOSE, ps)
            fields["PIN TYPE"].options = self.pin_types

            # submit form
            submit = self.pa.form(fields)
            if submit:
                self.cur.execute("UPDATE braids SET customer_pn = '"+submit["CUSTOMER PART NUMBER"]+"', flex_pn = '"+submit["FLEX PART NUMBER"]+"', size = "+str(submit["SIZE"])+", ps = '"+submit["PIN TYPE"]+"' WHERE test_cable_id = "+str(test_cable_id)+" AND braid_id = "+str(braid_id))
                self.con.commit()
                self.pa.print("Braid #"+str(test_cable_id)+"."+str(braid_id)+" - Changes have been saved")
            else:
                self.pa.error("Braid #"+str(test_cable_id)+"."+str(braid_id)+" - Changes have NOT been saved")

        # restart
        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()

    def delete(self):
        ## DELETE
        #- This will allow you to delete an existing barid only if it is the last one
        
        # get test cable id to edit
        ans = self.pa.input("What braid would you like to delete? [Insert in the following format: test_cable_id.braid_id (For example: 12.4)]")
        ans = ans.split(".")
        error = False
        if len(ans) != 2:
            self.pa.error("Error! Invalid input")
            error = True
        else:
            test_cable_id = ans[0]
            braid_id = ans[1]
        
        # check if test cable exists
        if not error:
            self.cur.execute("SELECT * FROM braids WHERE test_cable_id = "+test_cable_id)
            fetched_values = self.cur.fetchall()
            if len(fetched_values) == 0:
                error = True
                self.pa.error("Test cable: "+test_cable_id+" is not in the database")
        
        # check if braid exists
        if not error:
            self.cur.execute("SELECT * FROM braids WHERE test_cable_id = "+test_cable_id+" AND braid_id = "+braid_id)
            fetched_values = self.cur.fetchall()
            if len(fetched_values) == 0:
                error = True
                self.pa.error("Braid: "+braid_id+" in test cable: "+test_cable_id+" is not in the database")
            else:
                data = fetched_values[0]
                test_cable_id = data[0]
                braid_id = data[1]
        
        # check last
        if not error:
            if braid_id > 1:
                # make sure the braid is not the last one
                self.cur.execute("SELECT * FROM braids WHERE test_cable_id = "+str(test_cable_id)+" AND braid_id = "+str(braid_id+1))
                fetched_values = self.cur.fetchall()
                if len(fetched_values) != 0:
                    error = True
                    self.pa.error("Braid: "+str(braid_id)+" in test cable: "+str(test_cable_id)+" is not last")
            else:
                self.cur.execute("SELECT * FROM braids WHERE test_cable_id = "+str(test_cable_id+1))
                fetched_values = self.cur.fetchall()
                if len(fetched_values) != 0:
                    error = True
                    #print(fetched_values)
                    #print(test_cable_id)
                    self.pa.error("Test cable: "+str(test_cable_id)+" is not last")
        
        # delete
        if not error:
            self.cur.execute("SELECT * FROM braids WHERE test_cable_id = "+str(test_cable_id)+" AND braid_id = "+str(braid_id))
            fetched_values = self.cur.fetchall()
            #print(fetched_values)
            if len(fetched_values) != 0:
                if self.pa.question("Are you sure you want to delete braid: "+str(test_cable_id)+"."+str(braid_id)):
                    self.cur.execute("DELETE FROM braids WHERE test_cable_id = "+str(test_cable_id)+" AND braid_id = "+str(braid_id))
                    self.con.commit()
                    self.pa.print("Braid #"+str(test_cable_id)+"."+str(braid_id)+" was deleted")
                else:
                    self.pa.error("Braid #"+str(test_cable_id)+"."+str(braid_id)+" was NOT deleted")
            else:
                self.pa.error("Unexpected error!")

        # restart
        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()
"""
main()

# SCRIPT FUNCTIONS

# SETTINGS
# Database location --> The location of the user database. For example: database.db

# RELATED FILES