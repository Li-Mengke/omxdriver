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

def temp():
    if self.a > 0:
        gui('完成', '已经完成复制，可以取出U盘', '400x300')
        continue

    # 将需要复制位置的路径组合，命名为时间
    name_folder = os.path.join(self.target_folder, time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()))
    # 创建路径
    os.mkdir(name_folder)

    # 扫描文件夹
    try:
        for root, dirs, files in os.walk(self.scan_folder):
            if self.a == 0:
                print('start copy usb is {}'.format(root[0]))
            self.a += 1
            # print(a)
            if len(files) == 0:
                continue

            for name in files:

                file = os.path.join(root, name)
                if regex_filename.match(file) and os.path.getsize(file) < 1024 * 1024 * 2:
                    file_num += 1

                    print(file)
                    file_create_time = time.ctime(os.path.getctime(file))
                    file_create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file)))

                    shutil.copy2(file, name_folder)
                else:
                    continue
        if file_num == 0:
            print('usb is not found file')
            continue
        print('共下载{}份文件---用时:{}s'.format(file_num, time.time() - start_time))
        print(self.a)
    except Exception:
        print('here needs a Error-log')
        continue

class Usb_monitor(object):


    # 定义睡眠时间、U盘地址、复制目标文件夹、树莓派扫描源目录
    def __init__(self,sleep_time, usb_path, target_folder, scan_folder):
        self.sleep_time = sleep_time
        self.usb_path = usb_path
        self.target_folder = target_folder
        self.scan_folder = scan_folder
        self.a = 0
        self.active  = True
        self.active1 = True
        self.active2 = True

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

    def check_Task_dir(self):
        if os.path.exists(self.dir_of_udisk+"\\Task") is True:  # 如果保存地址不存在（os.path.exists()判断保存地址是否存在）
            self.active2 = False
        elif not(os.path.exists(self.dir_of_udisk+r'\Task')):
            gui('错误','请更换合适的的U盘','700x400')

    def create_report_folder(self):
        if not(os.path.exists(self.dir_of_udisk+r'\Report')):
            os.mkdir(self.dir_of_udisk+r'\Report')
            Mac_name = 'Mac-123456'
            os.mkdir(self.dir_of_udisk+r'\report\\'+Mac_name)

    def usb_monitor(self):
        # 设置需扫描的后缀名（后面看怎么改成函数）
        #regex_filename = re.compile(r'(.*txt$)|(.*log$)')  # |(.*docx$)|(.*ppt$)|(.*xls$)|(.*py$)')
        # 主循环
        while self.active:
            time.sleep(self.sleep_time)  # 推迟线程
            start_time = time.time()  # 开始时间
            file_num = 0

            #u盘检测
            while self.active2:
                self.plug_detection()
                self.get_dir_of_udisk()
                self.check_Task_dir()
            self.create_report_folder()









# 设置睡眠时间、U盘地址、复制目标文件夹、树莓派扫描源目录
Um=Usb_monitor(1,r'G:/tempp',r'G:/tempp',r'F:/temppp')
#   运行usb_monitor ，目前功能包括
#   1、检测U盘地址是否存在
#   2、检测树莓派扫描源目录获得所需要的后缀文件、
#   3、复制到目标文件夹
#   4、循环弹出GUI提示取出U盘
Um.usb_monitor()


