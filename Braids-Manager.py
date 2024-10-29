# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("Braids Manager", "1.0")

        # set-up main memu
        self.sc.add_main_menu_item("ADD NEW BRAID", self.new)
        self.sc.add_main_menu_item("LUA TO CSV", self.translate)

        # get settings
        self.path_main = self.sc.get_setting("Braids Folder")
        self.lbl_path = self.sc.get_setting("Labels Folder")

        # test all paths
        self.sc.test_path(self.path_main)
        self.sc.test_path(self.lbl_path)
        self.Labels = []
        self.Labels.append(self.lbl_path+"/LBL MPT AR00179 Braid number on plastic bag.btw")
        self.Labels.append(self.lbl_path+"/LBL MPT AR00179 Braid number on MPT side.btw")
        self.Labels.append(self.lbl_path+"/LBL MPT AR00179 Braid number on MPT side ABC.btw")
        self.Labels.append(self.lbl_path+"/LBL MPT AR00179 Braid number on product side.btw")
        self.Labels.append(self.lbl_path+"/LBL MPT AR00233 Hood Marker ABC.btw")
        self.Labels.append(self.lbl_path+"/LBL MPT AR00233 Hood Marker Numbers.btw")

        for lbl in self.Labels:
            self.sc.test_path(lbl)

        # load databases
        self.load_databases()

        # display main menu
        self.sc.start()

    def load_databases(self):
        # get current braid number
        self.BRAIDS = 0 
        for path, dirs, files in os.walk(self.path_main):
            for file in files:
                if ".csv" in file:
                    number = file[3:]
                    if os.path.isfile(self.path_main+"/"+file):
                        newid = number.split(".")
                        newid = newid[0]
                        try:
                            newid = int(newid)
                            if newid > self.BRAIDS:
                                self.BRAIDS = newid
                        except:
                            pass
        
        self.BRAIDS += 1

    def new(self):
        # load if number
        self.load_databases()

        # get number of mpt side plugs
        global_points = self.sc.input("For PLUG #"+str(self.BRAIDS)+" Insert number of MPT-SIDE PLUGS [1 Plug = 50 Global points]")

        # test user input
        try:
            global_points = int(global_points)
            global_points = global_points*50
        except:
            self.sc.error("Invalid input")
            self.sc.restart()
            return
        
        # get product side number of plugs
        plugs = self.sc.input("For PLUG #"+str(self.BRAIDS)+" Insert number of PRODUCT-SIDE PLUGS")

        # test user input
        try:
            plugs = int(plugs)
        except:
            self.sc.error("Invalid input")
            self.sc.restart()
            return
        
        # for every plug
        plugs_info = {}
        for i in range(1, plugs+1):
            part_number = self.sc.input("For PLUG #"+str(self.BRAIDS)+"."+str(i)+" Insert product-side-plug PART NUMBER").upper() or "None"
            rafael_part_number = self.sc.input("For PLUG #"+str(self.BRAIDS)+"."+str(i)+" Insert product-side-plug RAFAEL PART NUMBER").upper() or "None"
            pin_type = self.sc.choose("For PLUG #"+str(self.BRAIDS)+"."+str(i)+" Choose Insert product-side-plug PIN TYPE", ["Pin", "Socket", "Both", "NA"])
            plugs_info[i] = [str(i), part_number, rafael_part_number, pin_type]
        
        # make a map
        file = open(self.path_main+"/R1_"+str(self.BRAIDS)+".csv", 'w')
        file.write("GLOBAL POINT,PLUG,PIN,PLUG NUMBER,PART NUMBER,RAFAEL PART NUMBER,PIN TYPE\n")
        for i in range(1,global_points+1):
            if i in plugs_info:
                info = plugs_info[i]
            else:
                info = ["","","",""]
            file.write(str(i)+",,,"+info[0]+","+info[1]+","+info[2]+","+info[3]+"\n")
        file.close()
        os.popen(self.path_main+"/R1_"+str(self.BRAIDS)+".csv")
        for lbl in self.Labels:
            os.popen(lbl)
        
        # restart
        self.sc.restart()

    def translate(self):
        # get file path
        path_to_lua = self.sc.input("Insert path to .lua file you wish to convert to .csv")
        self.sc.test_path(path_to_lua)

        lua = open(path_to_lua,'r')
        lines = lua.readlines()
        lua.close()

        # read file data
        data = {}
        connector = ""
        status = None
        for line in lines:
            line = line.replace("\n", "")
            
            if status == None:
                if "connector_list" in line:
                    status = "get_branch_id"
            
            if status == "get_branch_id":
                if "name" in line:
                    line = line.split("[[")
                    line = line[1]
                    line = line.replace("]]", "")
                    line = line.replace(",", "")
                    line = line.split("_")
                    connector = line[2]
                    data[connector] = []
                    status = "wait_for_pins_command"
            
            if status == "wait_for_pins_command":
                if "pins" in line:
                    status = "collect_pins"
            
            if status == "collect_pins":
                if "name" in line and not "kelvin" in line:
                    if "{" in line:
                        line = line.split("{")
                        line = line[1]
                        line = line.split(",")
                        global_point = line[0]
                        pin = line[1]
                        pin = pin.replace("name","").replace(" ","").replace("=","").replace("[","").replace("]","").replace(",","").replace("}","")
                        data[connector].append((global_point, pin))
                    else:
                        line = line.split("[[")
                        line = line[1]
                        line = line.replace("]]", "")
                        line = line.replace(",", "")
                        line = line.split("_")
                        connector = line[2]
                        data[connector] = []
                        status = "wait_for_pins_command"
                if "name" in line and "kelvin" in line:
                    line = line.replace("name","").replace(" ","").replace("=","").replace("[","").replace("]","").replace("}","").replace("{","").replace("kelvin","")
                    line = line.split(",")
                    global_point = line[0]
                    pin = line[1]
                    data[connector].append((global_point, pin))
                    global_point = line[2]
                    data[connector].append((global_point, pin))
        
        # oragnize by global points
        size = int(global_point) / 50
        size = int(size)+1
        #print(size)
        #print(data)
        data_by_global_point = {} # GLOBAL POINT, PLUG, PIN, PLUG NUMBER, PART NUMBER, RAFAEL PART NUMBER,PIN TYPE
        for plug, pins in data.items():
            for pin in pins:
                data_by_global_point[pin[0]] = [pin[0], plug, pin[1], "", "", "", "",]
        
        for g in range(size):
            for gl in range(50):
                gl += g*50
                gl += 1
                if not str(gl) in data_by_global_point:
                    data_by_global_point[str(gl)] = [str(gl),"","","","","",""]
        #print(data_by_global_point)
        i = 0
        for connector in data.keys():
            i += 1
            ii = str(i)
            data_by_global_point[ii][3] = connector
            data_by_global_point[ii][4] = "None"
            data_by_global_point[ii][5] = "None"
            data_by_global_point[ii][6] = "NA"
        #print(data_by_global_point)
        sorted_data = []
        for pins in data_by_global_point.values():
            sorted_data.append((pins[0], pins[1], pins[2], pins[3], pins[4], pins[5], pins[6]))
        self.load_databases()
        filename = self.path_main+"/___test R1_"+str(self.BRAIDS)+".csv"
        file = open(filename, 'w')
        file.write("GLOBAL POINT,PLUG,PIN,PLUG NUMBER,PART NUMBER,RAFAEL PART NUMBER,PIN TYPE\n")
        for line in sorted_data:
            GLOBAL_POINT = line[0]
            PLUG = line[1]
            PIN = line[2]
            PLUGNUMBER = line[3]
            PARTNUMBER = line[4]
            RAFAELPARTNUMBER = line[5]
            PINTYPE = line[6]
            file.write(GLOBAL_POINT+","+PLUG+","+PIN+","+PLUGNUMBER+","+PARTNUMBER+","+RAFAELPARTNUMBER+","+PINTYPE+"\n")
        file.close()
        os.popen(filename)
        
        # restart
        self.sc.restart()
main()