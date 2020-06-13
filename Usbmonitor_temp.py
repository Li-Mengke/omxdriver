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
        self.regex_filename = re.compile(r'(.*json$)|(.*log$)')  # |(.*docx$)|(.*ppt$)|(.*xls$)|(.*py$)')

    #u盘插拔检测
    def plug_detection(self):
        while self.active1:
            for item in psutil.disk_partitions():
                if "removable" in item.opts: #在Linux上需要把removable 改成sda，下面同理
                    print("U盘插入")
                    self.active1 = False
                else:
                    print('not in')

    def get_dir_of_udisk(self):
        for i in psutil.disk_partitions():
            if 'removable' in i.opts:
                self.dir_of_udisk = i.device
                print(self.dir_of_udisk)

    #self.dir_of_udisk + r"\Task"
    def check_dir(self,path):
        if os.path.exists(path) is True:  # 如果保存地址不存在（os.path.exists()判断保存地址是否存在）
            self.active2 = False
        elif not(os.path.exists(path)):
            gui('错误','请更换合适的的U盘','700x400')

    def create_report_folder(self):
        if not(os.path.exists(self.dir_of_udisk+r'\Report')):
            os.mkdir(self.dir_of_udisk+r'\Report')
            Mac_name = 'Mac-123456'
            os.mkdir(self.dir_of_udisk+r'\report\\'+Mac_name)

    def get_copy_name(self):
        pass

    def scan_Task(self):
        try:
            scan_folder = self.dir_of_udisk + r'Task'
            for root, dirs, files in os.walk(scan_folder):
                if len(files) == 0:
                    print('len(files)==0')
                    continue
                for name in files:
                    file = os.path.join(root,name)
                    if self.regex_filename.match(file) and os.path.getsize(file) < 1024 * 1024 * 20:
                        self.file_num += 1
                        print(file)
                        if not(os.path.exists(r'F:\linshiwenjianjia')):
                            os.mkdir(r'F:\linshiwenjianjia')
                        name_folder = r'F:\linshiwenjianjia'
                        print(name_folder)

                        shutil.copy2(file,name_folder)

            if self.file_num == 0:
                print('usb is not found file')
                continue
            print('共下载{}份文件---用时:{}s'.format(self.file_num, time.time() - start_time))
        except Exception:
            print('here needs a Error-log')
            continue


    def usb_monitor(self):
        # 设置需扫描的后缀名（后面看怎么改成函数）

        # 主循环
        while self.active:
            time.sleep(1)  # 推迟线程
            global start_time
            start_time = time.time()  # 开始时间

            #u盘检测
            while self.active2:
                self.plug_detection()
                self.get_dir_of_udisk()
                Task_path = self.dir_of_udisk + r"Task"
                self.check_dir(Task_path)   #check Task
            self.create_report_folder()

            print(self.dir_of_udisk + r"Task")
            self.scan_Task()

Um=Usb_monitor()
Um.usb_monitor()


