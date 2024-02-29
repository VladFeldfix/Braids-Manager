-- Get Operator Name and Serial Number
if GetPersist('OperatorName') then OperatorName = GetPersist('OperatorName') else OperatorName = 'OperatorName' end 
if GetPersist('SerialNumber') then SerialNumber = GetPersist('SerialNumber') else SerialNumber = 'SerialNumber' end
OperatorName = InputText('Enter Operator Name',OperatorName, 'Operator Name', '')
SetPersist('OperatorName',OperatorName)
SerialNumber = InputText('Enter Serial Number',SerialNumber, 'Serial Number', '')
SetPersist('SerialNumber',SerialNumber)

-- Generate report header
Report.Header('Machine Name',"MPT-5000")
Report.Header('Test TRD',"PS-39-756948 Rev.: L")
Report.Header('Product Part Number',tostring("PARTNUMBER"))
Report.Header('Product Description',tostring("PRODUCT_DESCRIPTION"))
Report.Header('Wiring Diagram',tostring("DRAWING_PN")..'Rev.: '..tostring("DRAWING_REV"))
Report.Header('Written by',"Vlad Feldfix, Vladimir Shishkovsky")
Report.Header('Operator Name',tostring("OperatorName"))
Report.Header('Serial Number',tostring("SerialNumber"))

-- setup report file name
date_stamp = os.date('%d%b%Y')
str_date_stamp = date_stamp.upper(date_stamp)
SetReportFileName(SerialNumber..'-'..str_date_stamp..'-'..ProductName())