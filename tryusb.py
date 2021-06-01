# import win32api
# drives = win32api.GetLogicalDrives()
# print (drives)
# #drives = drives.split('\000')[:-1]
# #print (drives)
# for usb in wmi.InstancesOf("CIM_UserDevice"):
#      #print(usb.Manufacturer)
#      print(usb.Name)
# print("Другое: \n")
#print(usb.Manufacturer)
    # print('Name: ' + usb.Name)
    #print('ID:' + usb.DeviceID)
    #print('Description ' + str(usb.PNPDeviceID))
#     print('Class:' + str(usb.StatusInfo))
import win32com.client
wmi = win32com.client.GetObject("winmgmts:")
for objItem in wmi.InstancesOf("CIM_DiskDrive"):
    # print('Description ' + str(usb.Caption))
    if objItem.Caption != None:
        print("Caption: " + objItem.Caption)
    if objItem.MediaType != None:
        print(
        "MediaType: " + str( objItem.MediaType))
    if objItem.PNPDeviceID != None:
        print(
        "PNPDeviceID: " + str( objItem.PNPDeviceID))
    print("\n")

