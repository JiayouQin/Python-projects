"""
SDK:https://www.hikrobotics.com/cn/machinevision/service/download?module=0
作用：读取海康威视工业摄像头数据并输出图像
使用：下载开发SDK，找到MVS\Development\Samples\Python\BasicDemo，把MvImport文件夹放到该程序根目录下之后再执行！！！
开发目的：精简官方python Demo并让程序易读
调用输出图像：self.output_image默认为None，每更新一次会刷新为PIL图片，模式默认为rgb（259行）

what it does: read stream from HK industrial camera and output a image
Usage: download software SDK from the link above and find install path of MVS: MVS\Development\Samples\Python\BasicDemo, copy MvImport folder to the root path of this script.
reference output image: self.output_image in CameraOperation is None as default, each time a frame is updated it will be updated as an PIL image in RGB mode
"""

import sys,time,threading
sys.path.append("MvImport")
from MvCameraControl_class import *
import numpy as np
from PIL import Image
import ctypes


#ch:打开相机 | en:open device
class CameraOperation():
    def __init__(self,obj_cam,st_device_list,n_connect_num=0,b_open_device=False,b_start_grabbing = False,\
        h_thread_handle=None,b_thread_closed=False,st_frame_info=None,b_exit=False,b_save_bmp=False,\
        save_jpeg=False,buf_save_image=None,n_save_image_size=0,n_win_gui_id=0,frame_rate=0,\
        exposure_time=0,gain=0):
        self.connected = False
        self.save_jpeg = None
        self.obj_cam = obj_cam
        self.b_open_device = b_open_device
        self.n_connect_num = n_connect_num
        self.st_device_list = st_device_list
        self.b_start_grabbing = False
        self.output_image = None
        self.stream = False
        self.gain = gain
        self.numArray = None
        self.refreshed = False
    def Color_numpy(self,data,nWidth,nHeight): #把流数据转换为np阵列
        data_ = np.frombuffer(data, count=int(nWidth*nHeight*3), dtype=np.uint8, offset=0)
        numArray = np.zeros([nHeight, nWidth, 3],"uint8")
        numArray[:, :, 0] = data_[0:nWidth*nHeight*3:3].reshape(nHeight, nWidth) #r
        numArray[:, :, 1] = data_[1:nWidth*nHeight*3:3].reshape(nHeight, nWidth) #g
        numArray[:, :, 2] = data_[2:nWidth*nHeight*3:3].reshape(nHeight, nWidth) #b
        return numArray

    def Save_jpg(self,buf_cache):
        if(None == buf_cache):
            print('empty cache')
            return
        self.buf_save_image = None
        self.n_save_image_size = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048
        if self.buf_save_image is None:
            self.buf_save_image = (c_ubyte * self.n_save_image_size)()

        stParam = MV_SAVE_IMAGE_PARAM_EX()
        stParam.enImageType = MV_Image_Jpeg;                                        # ch:需要保存的图像类型 | en:Image format to save
        stParam.enPixelType = self.st_frame_info.enPixelType                               # ch:相机对应的像素格式 | en:Camera pixel type
        stParam.nWidth      = self.st_frame_info.nWidth                                    # ch:相机对应的宽 | en:Width
        stParam.nHeight     = self.st_frame_info.nHeight                                   # ch:相机对应的高 | en:Height
        stParam.nDataLen    = self.st_frame_info.nFrameLen
        stParam.pData       = cast(buf_cache, POINTER(c_ubyte))
        stParam.pImageBuffer=  cast(byref(self.buf_save_image), POINTER(c_ubyte)) 
        stParam.nBufferSize = self.n_save_image_size                                 # ch:存储节点的大小 | en:Buffer node size
        stParam.nJpgQuality = 80;                                                    # ch:jpg编码，仅在保存Jpg图像时有效。保存BMP时SDK内忽略该参数
        return_code = self.obj_cam.MV_CC_SaveImageEx2(stParam)            

        if return_code != 0:
            print('show error','save jpg fail! ret = '+self.To_hex_str(return_code))
            return 
        file_path = 'pic/temp.jpg' if self.save_jpeg == 'temp' else f"pic/{self.st_frame_info.nFrameNum}.jpg"
        print('file_path')
        file_open = open(file_path.encode('ascii'), 'wb+')
        img_buff = (c_ubyte * stParam.nImageLen)()
        try:
            cdll.msvcrt.memcpy(byref(img_buff), stParam.pImageBuffer, stParam.nImageLen)
            file_open.write(img_buff)
            print('show info','save jpg success!')
            self.save_jpeg = None
        except:
            raise Exception("get one frame failed:")
        if img_buff != None:
            del img_buff
        if self.buf_save_image != None:
            del self.buf_save_image

    def Get_parameter(self):
        if True == self.b_open_device:
            stFloatParam_FrameRate =  MVCC_FLOATVALUE()
            memset(byref(stFloatParam_FrameRate), 0, sizeof(MVCC_FLOATVALUE))
            stFloatParam_exposureTime = MVCC_FLOATVALUE()
            memset(byref(stFloatParam_exposureTime), 0, sizeof(MVCC_FLOATVALUE))
            stFloatParam_gain = MVCC_FLOATVALUE()
            memset(byref(stFloatParam_gain), 0, sizeof(MVCC_FLOATVALUE))
            ret = self.obj_cam.MV_CC_GetFloatValue("AcquisitionFrameRate", stFloatParam_FrameRate)
            if ret != 0:
                print('show error','get acquistion frame rate fail! ret = '+self.To_hex_str(ret))
            self.frame_rate = stFloatParam_FrameRate.fCurValue
            ret = self.obj_cam.MV_CC_GetFloatValue("ExposureTime", stFloatParam_exposureTime)
            if ret != 0:
                print('show error','get exposure time fail! ret = '+self.To_hex_str(ret))
            self.exposure_time = stFloatParam_exposureTime.fCurValue
            ret = self.obj_cam.MV_CC_GetFloatValue("Gain", stFloatParam_gain)
            if ret != 0:
                print('show error','get gain fail! ret = '+self.To_hex_str(ret))
            self.gain = stFloatParam_gain.fCurValue
            print('show info','get parameter success!')


    def Set_parameter(self,frameRate,exposureTime,gain):
        if '' == frameRate or '' == exposureTime or '' == gain:
            print('show info','please type in the text box !')
            return
        if self.b_open_device == True:
            ret = self.obj_cam.MV_CC_SetFloatValue("ExposureTime",float(exposureTime))
            if ret != 0:
                print('show error','set exposure time fail! ret = '+self.To_hex_str(ret))
            ret = self.obj_cam.MV_CC_SetFloatValue("Gain",float(gain))
            if ret != 0:
                print('show error','set gain fail! ret = '+self.To_hex_str(ret))
            ret = self.obj_cam.MV_CC_SetFloatValue("AcquisitionFrameRate",float(frameRate))
            if ret != 0:
                print('show error','set acquistion frame rate fail! ret = '+self.To_hex_str(ret))

            print('show info','set parameter success!')


    def Open_device(self):
        if False == self.b_open_device:
            # ch:选择设备并创建句柄 | en:Select device and create handle
            stDeviceList = cast(self.st_device_list.pDeviceInfo[int(self.n_connect_num)], POINTER(MV_CC_DEVICE_INFO)).contents
            self.obj_cam = MvCamera()
            ret = self.obj_cam.MV_CC_CreateHandle(stDeviceList)
            if ret != 0:
                self.obj_cam.MV_CC_DestroyHandle()
                print('show error','create handle fail! ret = '+ self.To_hex_str(ret))

            ret = self.obj_cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
            if ret != 0:
                print('show error','open device fail! ret = '+ self.To_hex_str(ret))

            print ("open device successfully!")
            self.b_open_device = True
            self.b_thread_closed = False

            # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
            if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
                nPacketSize = self.obj_cam.MV_CC_GetOptimalPacketSize()
                if int(nPacketSize) > 0:
                    ret = self.obj_cam.MV_CC_SetIntValue("GevSCPSPacketSize",nPacketSize)
                    if ret != 0:
                        print ("warning: set packet size fail! ret[0x%x]" % ret)
                else:
                    print ("warning: set packet size fail! ret[0x%x]" % nPacketSize)

            stBool = c_bool(False)
            ret =self.obj_cam.MV_CC_GetBoolValue("AcquisitionFrameRateEnable", stBool)
            if ret != 0:
                print ("get acquisition frame rate enable fail! ret[0x%x]" % ret)

            # ch:设置触发模式为off | en:Set trigger mode as off
            ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
            if ret != 0:
                print ("set trigger mode fail! ret[0x%x]" % ret)
            return 0

    def To_hex_str(self,num):
        chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
        hexStr = ""
        if num < 0:
            num = num + 2**32
        while num >= 16:
            digit = num % 16
            hexStr = chaDic.get(digit, str(digit)) + hexStr
            num //= 16
        hexStr = chaDic.get(num, str(num)) + hexStr   
        return hexStr

    def Start_grabbing(self):
        if self.stream == False and self.connected == True:
            if g.ui.feedback_mode.currentIndex() == 0:
                ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode",0) #set trigger mode to continuous
                print(f'set to continuous, success:{ret==0}')
                ret = self.obj_cam.MV_CC_StartGrabbing()
                print(f'start grabbing, success:{ret==0}')
            else:
                ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode",1)
                if ret != 0:
                    print('show error','set triggermode fail! ret = '+self.To_hex_str(ret))
                ret = self.obj_cam.MV_CC_SetEnumValue("TriggerSource",7)
                if ret != 0:
                    print('show error','set triggersource fail! ret = '+self.To_hex_str(ret))
                ret = self.obj_cam.MV_CC_StartGrabbing()
            self.stream = True
            self.b_start_grabbing = True
            self.cam_thread = threading.Thread(target=self.Work_thread)
            self.cam_thread.start()

    def Trigger_once(self):
        ret = self.obj_cam.MV_CC_SetCommandValue("TriggerSoftware")
        if ret != 0:
            print('show error','set triggersoftware fail! ret = '+self.To_hex_str(ret))


    def Stop_grabbing(self):#退出线程
        if  self.stream == True:
            self.stream = False
            self.cam_thread.join()
            ret = self.obj_cam.MV_CC_StopGrabbing()
            if ret != 0:
                print(f'show error','stop grabbing fail! ret ={ret}}')
            else:
                print ("stop grabbing successfully!")
            
    def Work_thread(self):
        stOutFrame = MV_FRAME_OUT()  
        img_buff = None
        buf_cache = None
        numArray = None
        while g.ui.button_start_stream.property('on') and g.run:
            if self.stream == False:
                break

            ret = self.obj_cam.MV_CC_GetImageBuffer(stOutFrame, 1000)
            if 0 == ret:
                if buf_cache==None:
                    buf_cache = (c_ubyte * stOutFrame.stFrameInfo.nFrameLen)()
                #获取到图像的时间开始节点获取到图像的时间开始节点
                self.st_frame_info = stOutFrame.stFrameInfo
                cdll.msvcrt.memcpy(byref(buf_cache), stOutFrame.pBufAddr, self.st_frame_info.nFrameLen)
                print (f"get one frame: Width[{self.st_frame_info.nWidth}], Height[{self.st_frame_info.nHeight}], nFrameNum[{self.st_frame_info.nFrameNum}]")
                self.n_save_image_size = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048
                if img_buff is None:
                    img_buff = (c_ubyte * self.n_save_image_size)()

                
                if self.save_jpeg:
                    print('trying to save jpg file')
                    self.Save_jpg(buf_cache) #ch:保存Jpg图片 | en:Save Jpg
                    
            else:
                print(f"no data")
                continue
            stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
            memset(byref(stConvertParam), 0, sizeof(stConvertParam))
            stConvertParam.nWidth = self.st_frame_info.nWidth
            stConvertParam.nHeight = self.st_frame_info.nHeight
            stConvertParam.pSrcData = cast(buf_cache, POINTER(c_ubyte))
            stConvertParam.nSrcDataLen = self.st_frame_info.nFrameLen
            stConvertParam.enSrcPixelType = self.st_frame_info.enPixelType 

            # RGB直接显示
            if PixelType_Gvsp_RGB8_Packed == self.st_frame_info.enPixelType:
                numArray = CameraOperation.Color_numpy(self,buf_cache,self.st_frame_info.nWidth,self.st_frame_info.nHeight)
            else:
                nConvertSize = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3
                stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
                stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
                stConvertParam.nDstBufferSize = nConvertSize
                time_start=time.time()
                ret = self.obj_cam.MV_CC_ConvertPixelType(stConvertParam)
                print('MV_CC_ConvertPixelType:',time.time() - time_start) 
                if ret != 0:
                    print('show error','convert pixel fail! ret = '+self.To_hex_str(ret))
                    continue
                cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
                self.numArray = CameraOperation.Color_numpy(self,img_buff,self.st_frame_info.nWidth,self.st_frame_info.nHeight)
                self.output_image = Image.fromarray(numArray, mode='RGB')
                self.refreshed = True
            #-------------------free buffer----------------------
            nRet = self.obj_cam.MV_CC_FreeImageBuffer(stOutFrame)


deviceList = MV_CC_DEVICE_INFO_LIST()
cam = MvCamera()
ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, deviceList)
obj_cam_operation = CameraOperation(cam,deviceList,0)

def reconnect():
    print('reset cam')
    obj_cam_operation.st_device_list = MV_CC_DEVICE_INFO_LIST()
    ret = obj_cam_operation.obj_cam.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, obj_cam_operation.st_device_list)
    print (f"found {obj_cam_operation.st_device_list.nDeviceNum} devices.")
    print(f'ret: {ret}')
    if ret != 0 or obj_cam_operation.st_device_list.nDeviceNum == 0:
        print('show info','no device found.')
    else:
        print (f"found {deviceList.nDeviceNum} devices.")
        obj_cam_operation.connected = True
        obj_cam_operation.Open_device()

def run():
    obj_cam_operation.Open_device()
    obj_cam_operation.Start_grabbing()

if __name__ == 'main':
    run()
