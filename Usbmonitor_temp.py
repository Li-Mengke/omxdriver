import os, time, shutil, re
import tkinter as tk
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

#设置需扫描的后缀名（后面看怎么改成函数）

regex_filename = re.compile(r'(.*txt$)|(.*log$)') #|(.*docx$)|(.*ppt$)|(.*xls$)|(.*py$)')
#*******************
#身份验证（需要替换方式）
#*******************
def check_admin(admin_path):
    admin_name = 'admin.txt'
    if os.path.exists(admin_path):
        for root, dirs, files in os.walk(admin_path):
            if admin_name in dirs:
                print('a')

# 设置睡眠时间、U盘地址、复制目标文件夹、树莓派扫描源目录
def usb_monitor(sleep_time, usb_path, target_folder,scan_folder):

# 标志复制是否成功
    a= 0
# 主循环
    while True:

        time.sleep(sleep_time)  # 推迟线程
        start_time = time.time()  # 开始时间
        file_num = 0  # 文件计数标志位

        # 返回U盘的地址名到u
        # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
        # 它不包括 . 和 .. 即使它在文件夹中。在linux系统中需要用list.sort()排序

        try:
            if not os.path.exists(target_folder):  # 如果保存地址不存在（os.path.exists()判断保存地址是否存在）
                os.mkdir(target_folder)  # 则创建一级目录（创建保存地址）os.makedirs()创建多级目录
            u = os.listdir(usb_path)
        except FileNotFoundError:  # 如果该地址名有文件或文件夹则意味着没有插入U盘，打印错误
            print('usb is not found')
            a = 0
            continue
        # 如果复制完成则打印U盘已经复制过了
        if a > 0:
            gui('完成','已经完成复制，可以取出U盘','400x300')
            continue

        # 将需要复制位置的路径组合，命名为时间
        name_folder = os.path.join(target_folder, time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()))
        # 创建路径
        os.mkdir(name_folder)

        # 扫描文件夹
        for root, dirs, files in os.walk(scan_folder):
            if a == 0:
                print('start copy usb is {}'.format(root[0]))
                #usb_name = dirs[0]
            a += 1
            print(a)
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
        print(a)
#验证身份
check_admin(r'G:/admin')
#USBmonitor (设置睡眠时间、U盘地址、复制目标文件夹、树莓派扫描源目录)
usb_monitor(1,r'G:/tempp',r'G:/tempp',r'F:/temppp')
