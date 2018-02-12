import ctypes

testDll = ctypes.WinDLL(r"C:\Users\Alen\Documents\repos\bin2txtswps\experimental\test_scripts\Axabffio32.dll")


hllApi = hllApiProto (("ABF_ReadOpen", testDll))

print(testDll)