from SmartConsole import *

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("Braids Manager", "4.0")

        # set-up main memu
        self.sc.add_main_menu_item("ADD NEW BRAID", self.new)

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
                    if os.path.isfile(self.path_main+"/"+file):
                        newid = file.split(".")
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
        file = open(self.path_main+"/"+str(self.BRAIDS)+".csv", 'w')
        file.write("GLOBAL POINT,PLUG,PIN,PLUG NUMBER,PART NUMBER,RAFAEL PART NUMBER,PIN TYPE\n")
        for i in range(1,global_points+1):
            if i in plugs_info:
                info = plugs_info[i]
            else:
                info = ["","","",""]
            file.write(str(i)+",,,"+info[0]+","+info[1]+","+info[2]+","+info[3]+"\n")
        file.close()
        os.popen(self.path_main+"/"+str(self.BRAIDS)+".csv")
        for lbl in self.Labels:
            os.popen(lbl)
        
        # restart
        self.sc.restart()

main()