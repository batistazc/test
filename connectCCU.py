from cgi import print_environ_usage
import paramiko, logging, time, subprocess

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='patrol_CCU.log', level=logging.INFO, format=LOG_FORMAT)

ssh = paramiko.SSHClient()
print("start")
logging.info("start run")
for i in range(300):
    #打印次数
    logging.warning(i+1)
    print(i+1)

    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # # 自动输入yes
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # 建立连接
    ssh.connect(hostname = "192.168.1.200", username = "patrol", port = 22, password = "patrol")
    
    # 执行命令并日志记录输出
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("date")
    logging.warning(ssh_stdout.read())

    # 执行命令并日志记录输出
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("journalctl -b | grep 'Found ordering cycle'")
    logging.error(ssh_stdout.read())

    # 执行命令并日志记录输出
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cat /vendor/build.prop")
    logging.info(ssh_stdout.read())

    # 执行命令并日志记录输出
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("top -b -i -n 2 | grep camera_service")
    # logging.info(ssh_stdout.read())

    #延迟重启
    time.sleep(2)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("reboot")
    logging.info("reboot ed")

    #等待重启
    time.sleep(200)
print("done")
logging.info("done")
