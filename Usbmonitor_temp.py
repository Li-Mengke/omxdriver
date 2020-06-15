import os, time, shutil, re
import tkinter as tk
import psutil
#设置窗口标题、文本、窗口大小
def gui(root_title,root_label,geometry):

    root_window = tk.Tk()
    root_window.title(root_title)
    root_window.geometry(geometry)

    main_frame = tk.Frame(root_window)
    main_label = tk.Label(main_frame,text = root_label)
    main_label.pack()

    main_frame.pack(expand = 'yes')
    root_window.mainloop()


class Usb_monitor(object):


    def __init__(self):
        self.file_num = 0
        self.active  = True
        self.active1 = True
        self.active2 = True
        self.regex_filename = re.compile(r'(.*json$)|(.*log$)')

    #u盘插拔检测
    def plug_detection(self):
        while self.active1:
            for item in psutil.disk_partitions():
                if "removable" in item.opts: #在Linux上需要把removable 改成sda，下面同理
                    print("U盘插入")
                    self.active1 = False
                else:
                    print('not in')

    # 获取可移动U盘路径
    import psutil
    def get_dir_of_udisk(self):
        if self.system_name == 'Windows':
            # 获取所有盘符信息
            disk_list = psutil.disk_partitions()
            self.u_path = [disk.device for disk in disk_list if disk.opts == 'rw,removable']
            if self.u_path:
                self.dir_of_udisk =  self.u_path[0]
        elif self.system_name == 'linux':
            import pyudev
            self.context = pyudev.Context()
            self.removable = [device for device in self.context.list_devices(subsystem='block', DEVTYPE='disk') if
                         device.attributes.asstring('removable') == "1"]
            for device in self.removable:
                partitions = [device.device_node for device in
                              context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
                # print("All removable partitions: {}".format(",
                # ".join(partitions)))
                # print("Mounted removable partitions:")
                for p in psutil.disk_partitions():
                    if p.device in partitions:
                        self.dir_of_udisk = p.mountpoint

#    def get_dir_of_udisk(self):
 #       for i in psutil.disk_partitions():
  #          if 'removable' in i.opts:
   #             self.dir_of_udisk = i.device
    #            print(self.dir_of_udisk)

    #self.dir_of_udisk + r"\Task"
    def check_dir(self,path):
        if os.path.exists(path) is True:  # 如果保存地址不存在（os.path.exists()判断保存地址是否存在）
            self.active2 = False
        elif not(os.path.exists(path)):
            gui('错误','请更换合适的的U盘','700x400')

    def Mac_name(self):
        self.mac_name = 'kz-mac-4'

    def create_report_folder(self):
        if not(os.path.exists(self.dir_of_udisk+r'\Report')):
            os.mkdir(self.dir_of_udisk+r'\Report')
            os.mkdir(self.dir_of_udisk+r'\report\\'+self.mac_name)

    def decode_json(self):    #(从json解析出上刊、下刊、监播任务要求，
        import json

        with open('kz-mac-4.json', encoding='utf-8') as f:
            # filedata是一个list,内容的类型是字典
            filedata = json.load(f)
            self.plist = []
            self.dlist = []
        # print(filedata)
        # 将filedata的每项解析为q（字典）并做处理
        for i in range(len(filedata)):
            # print(filedata[i],'\n')
            q = filedata[i]
            if q['messageType'] == 'putinto-task':
                content = q['content']  # putinto-task的内容是一个列表
                for l in range(len(content)):  # 解析content
                    if 'materialName' in content[l]:
                        # lcon 是上刊名列表
                        self.plist.append(content[l]['materialName'])
                # put_into_task()
                # ********'这里加上日志'
            # else:
            elif q['messageType'] == 'down-task':
                for l in range(len(content)):  # 解析content
                    if 'materialName' in content[l]:
                        # dlist 是上刊名列表
                        self.dlist.append(content[l]['materialName'])

    def put_into_task(self):
        scan_folder = self.dir_of_udisk + r'Task\\'
        for root, dirs, files in os.walk(scan_folder):
            for name in self.plist:
                if name in files:
                    self.file_num += 1
                    print(self.file_num)
                    if not (os.path.exists(r'F:\Task')):
                        os.mkdir(r'F:\Task')
                        if not (os.path.exists(r'F:\Task\video')):
                            os.mkdir(r'F:\Task\video')
                    name_folder = r'F:\Task\video'
                    shutil.copy2(scan_folder+'video\\'+name,name_folder)
        thistime = '复制已经完成---用时:{}s'.format(time.time() - start_time)

        gui('复制完成',thistime,'700x500')

    def down_task(self):
        scan_folder = r'F:\Task\video'
        for root, dirs, files in os.walk(scan_folder):
            for name in self.dlist:
                if name in files:
                    target_name = scan_folder+'\\'+name
                if os.path.exists(target_name):
                    print('daozhe')
                    os.remove(target_name)


                '''
                
                for name in files:
                    file = os.path.join(root,name)
                    print(file)
                    if self.regex_filename.match(file) and os.path.getsize(file) < 1024 * 1024 * 20:
                        self.file_num += 1
                        print(file)
                        if not(os.path.exists(r'F:\linshiwenjianjia')):
                            os.mkdir(r'F:\linshiwenjianjia')
                        name_folder = r'F:\linshiwenjianjia'
                        print(name_folder)

                        shutil.copy2(file,name_folder)
'''
            if self.file_num == 0:
                print('usb is not found file')
       # except Exception:
        #    print('here needs a Error-log')

    def monitor_task(self):
        raise NotImplementedError

    def db_create_table(self):
        raise NotImplementedError


    def usb_monitor(self):
        # 设置需扫描的后缀名（后面看怎么改成函数）

        # 主循环
        while self.active:
            time.sleep(1)  # 推迟线程
            global start_time
            start_time = time.time()  # 开始时间
            self.system_name = 'Windows'
            self.Mac_name()

            #u盘检测
            while self.active2:
                self.plug_detection()
                self.get_dir_of_udisk()
                Task_path = self.dir_of_udisk + r"Task"
                self.check_dir(Task_path)   #check Task
            self.create_report_folder()
            self.decode_json()
            print(self.plist,self.dlist)
            print(self.dir_of_udisk + r"Task")
            self.scan_Task()
            self.scan_pi()

Um=Usb_monitor()
Um.usb_monitor()


