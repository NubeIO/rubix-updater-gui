import logging
import os

import githubdl
from datetime import datetime

from fabric import Connection
from invoke import Responder

from app.core.commands import LinuxCommands
from app.core.logger import LoggerSetup
from app.core.make_connection import SSHConnection
from app.core.tasks_rubix import file_transfer_stm, file_transfer_stm_build, deploy_rubix_update, command_ls, \
    deploy_rubix_service_update, reboot_host, install_rubix_app, task_command_blank, bbb_env_transfer
from app.utils.utils import Utils
from config.load_config import get_config_host, get_config_rubix_service, get_config_bios, get_bbb_host_config

_get_config_host = get_config_host()
_rubix_settings = get_config_rubix_service()
_host_settings = get_config_host()
_bios_settings = get_config_bios()
_bbb_settings = get_bbb_host_config()

RUBIX_IMAGE_REPO = "https://github.com/NubeIO/rubix-pi-image"
RUBIX_SERVICE_CONFIG = "config-files/rubix-apps"
RUBIX_SERVICE_DIR = '/data/rubix-service/config'
POINT_SERVER_CONFIG = "config-files/point-server"
STM_FLASH_SCRIPT = "scripts/rubix"
STM_FLASH_BUILD = "builds"
POINT_SERVER_PATH = "./config-files/point-server/point-server/config.json"
BACNET_SERVER_PATH = "./config-files/bacnet-server/bacnet-server"
HOME_DIR = '/home/pi'
WIRES_DATA_DIR = '/data/rubix-wires/config'
CWD = os.getcwd()


class RubixUpdateLogger:
    def __init__(self, parent):
        self.parent = parent
        LoggerSetup(self.parent)


class ScratchPadController:
    def __init__(self, parent, app):
        self.parent = parent
        RubixUpdateLogger(self.parent)
        self.app = app
        # use config
        self.parent.use_config_file.toggled.connect(self._use_config)
        self.parent.use_config_file.setChecked(True)
        self.parent.setting_remote_update_host.setEnabled(False)
        self.parent.setting_remote_update_port.setEnabled(False)
        self.parent.setting_remote_update_user.setEnabled(False)
        self.parent.setting_remote_update_password.setEnabled(False)
        self.parent.rubix_username.setEnabled(False)
        self.parent.rubix_password.setEnabled(False)
        self.parent.rubix_bios_port.setEnabled(False)
        self.parent.rubix_service_port.setEnabled(False)
        self.parent.github_token.setEnabled(False)
        # tab host connection
        self.parent.action_remote_update_connect.pressed.connect(self._check_rc_connection)
        # self.parent.action_remote_ping_host.pressed.connect(self._ping_host)
        # update rubix bios
        self.parent.action_remote_update.pressed.connect(self._update_rubix)
        self.parent.action_remote_update.setEnabled(False)
        # update rubix service
        self.parent.action_remote_rubix_service.pressed.connect(self._update_rubix_service)
        self.parent.action_remote_rubix_service.setEnabled(False)
        # flash lora
        self.parent.action_lora_reflash.pressed.connect(self._lora_reflash)
        # check bbb connection
        self.parent.bbb_connect.pressed.connect(self.check_bbb_connection)
        # update bbb ip
        self.parent.run_update_bbb_ip.setEnabled(False)
        self.parent.run_update_bbb_ip.pressed.connect(self.run_update_bbb_ip)
        # env file bbb
        self.parent.bbb_transfer_env.pressed.connect(self.bbb_send_env)
        # rubix_reboot
        self.parent.rubix_reboot.pressed.connect(self._reboot_rubix)
        # install/restart rubix app
        self.parent.rubix_app_action_run.pressed.connect(self._manage_rubix_app)
        # modpoll
<<<<<<< HEAD
        # self.parent.rubix_app_action_run.pressed.connect(self._manage_rubix_app)
=======
        self.parent.mod_connect.pressed.connect(self._modpoll_lora)
>>>>>>> f0b3f36d7edefae827aa34267401149f5c782de6

    def _connection(self):
        host = self.parent.setting_remote_update_host.text()
        port = self.parent.setting_remote_update_port.text()
        user = self.parent.setting_remote_update_user.text()
        password = self.parent.setting_remote_update_password.text()
        time = self._time_stamp()
        use_config = self.parent.use_config_file.isChecked()
        cx = SSHConnection(
            host=host,
            port=port,
            user=user,
            connect_timeout=5,
            password=password,
            use_config=use_config
        ).connect()
        if not cx:
            return False
        else:
            return cx

    def _use_config(self):
        use_config = self.parent.use_config_file.isChecked()
        # test
        if use_config:
            self.parent.setting_remote_update_host.setEnabled(False)
            self.parent.setting_remote_update_port.setEnabled(False)
            self.parent.setting_remote_update_user.setEnabled(False)
            self.parent.setting_remote_update_password.setEnabled(False)
            self.parent.rubix_username.setEnabled(False)
            self.parent.rubix_password.setEnabled(False)
            self.parent.rubix_bios_port.setEnabled(False)
            self.parent.rubix_service_port.setEnabled(False)
            self.parent.github_token.setEnabled(False)
        else:
            self.parent.setting_remote_update_host.setEnabled(True)
            self.parent.setting_remote_update_port.setEnabled(True)
            self.parent.setting_remote_update_user.setEnabled(True)
            self.parent.setting_remote_update_password.setEnabled(True)
            self.parent.rubix_username.setEnabled(True)
            self.parent.rubix_password.setEnabled(True)
            self.parent.rubix_bios_port.setEnabled(True)
            self.parent.rubix_service_port.setEnabled(True)
            self.parent.github_token.setEnabled(True)

    def _check_rc_connection(self):
        cx = self._connection()
        if not cx:
            self.parent.action_remote_update.setEnabled(False)
            self.parent.action_remote_rubix_service.setEnabled(False)
        else:
            self.parent.action_remote_update.setEnabled(True)
            self.parent.action_remote_rubix_service.setEnabled(True)

    def _connection_bbb(self):
        use_config = self.parent.bbb_use_config_file.isChecked()
        if use_config:
            host = _bbb_settings.get('get_bbb_host')
            port = _bbb_settings.get('get_bbb_port')
            user = _bbb_settings.get('get_bbb_user')
            password = _bbb_settings.get('get_bbb_password')
        else:
            # ip = self.parent.setting_remote_update_host.text()
            host = self.parent.bbb_host.text()
            port = self.parent.bbb_port.text()
            user = self.parent.bbb_username.text()
            password = self.parent.bbb_password.text()
        time = self._time_stamp()
        logging.info(f"try and connect with host:{host} port:{port} user:{user}")
        cx = SSHConnection(
            host=host,
            port=port,
            user=user,
            connect_timeout=5,
            password=password
        ).connect()
        if not cx:
            msg = f"device on ip: {host} is DEAD {time}"
            self.parent.statusBar.showMessage(msg)
            return False
        else:
            msg = f"device on ip: {host} is connected {time}"
            self.parent.statusBar.showMessage(msg)
            return cx

    def _connection_status(self):
        cx = self._connection()
        ip = self.parent.setting_remote_update_host.text()
        time = self._time_stamp()
        if not cx:
            msg = f"device on ip: {ip} is DEAD {time}"
            self.parent.statusBar.showMessage(msg)
            return False
        else:
            msg = f"device on ip: {ip} is connected {time}"
            self.parent.statusBar.showMessage(msg)
            return cx

    def _lora_reflash(self):
        cx = self._connection()
        github_token = self.parent.github_token.text()
        githubdl.dl_dir(RUBIX_IMAGE_REPO, STM_FLASH_SCRIPT,
                        github_token=github_token)
        file_stm_script = f"{CWD}/{STM_FLASH_SCRIPT}/rubix/stm-flasher.py"
        self.parent.statusBar.showMessage(f"LOG: DOWNLOAD STM SCRIPT")
        githubdl.dl_dir(RUBIX_IMAGE_REPO, STM_FLASH_BUILD,
                        github_token=github_token)
        file_stm_bin = f"{CWD}/{STM_FLASH_BUILD}/r-c-loraraw_subnet-1_v0.2.bin"
        file_transfer_stm(cx, file_stm_script, HOME_DIR)
        self.parent.statusBar.showMessage(f"LOG: START STM INSTALL")
        file_transfer_stm_build(cx, file_stm_bin, HOME_DIR)

    def _manage_rubix_app(self):
        use_config = self.parent.use_config_file.isChecked()
        add_config_file = self.parent.rubix_app_use_config.isChecked()
        app = self.parent.rubix_app_selection.currentText()
        action = self.parent.rubix_app_action.currentText()
        version = "latest"
        if use_config:
            ip = _host_settings.get('get_host')
            link = f"""<a href="http://{ip}:1414">open {ip}:1414</a>"""
            self.parent.rubix_plat_hyperlink.setText(link)
        else:
            ip = self.parent.setting_remote_update_host.text()
            link = f"""<a href="http://{ip}:1414">open {ip}:1414</a>"""
            self.parent.rubix_plat_hyperlink.setText(link)
        ping = Utils.ping(ip)
        if ping:
            install_rubix_app(ip, version, app, add_config_file, action)
            msg = f"RUN APP TASK PASS:  rubix apps task: {action} app: {app} on ip: {ip}"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            return msg
        else:
            msg = f"RUN APP TASK FAIL: rubix apps task: {action} app: {app} on ip: {ip}"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            return msg

    def _update_rubix(self):
        cx = self._connection()
        use_config = self.parent.use_config_file.isChecked()
        if use_config:
            ip = _host_settings.get('get_host')
        else:
            ip = self.parent.setting_remote_update_host.text()
        ping = Utils.ping(ip)
        if ping:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            logging.info("------ Connect and start updates ------")
            deploy_rubix_update(cx)
            msg = f"install completed"
            logging.info(msg)
            return msg
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            return msg

    def _modpoll_reg_type(self, reg_type):
        if reg_type == "READ-DO-COIL":
            return 0
        elif reg_type == "READ-DI-INPUT":
            return 1
        elif reg_type == "READ-AO-HOLDING":
            return 4
        elif reg_type == "READ-AI-INPUT":
            return 3

    def _modpoll_data_type(self, reg_type):
        if reg_type == "raw":
            return "raw"
        elif reg_type == "hex":
            return "hex"
        elif reg_type == "int":
            return "int"
        elif reg_type == "float":
            return "float"
        elif reg_type == "mod":
            return "mod"


    def _modpoll_lora(self):
        # cx = self._connection()
        mod_run_for = self.parent.mod_run_for.text()
        mod_serial_port = self.parent.mod_serial_port.currentText()
        mod_baud_rate = self.parent.mod_baud_rate.currentText()
        mod_device_address = self.parent.mod_device_address.text()
        mod_point_address = self.parent.mod_point_address.text()
        mod_length = self.parent.mod_length.text()
        mod_point_type = self.parent.mod_point_type.currentText()
        mod_data_type = self.parent.mod_data_type.currentText()
        mod_delay = self.parent.mod_delay.text()
        mod_delay = int(mod_delay)*1000
        ping = True
        mod_point_type = self._modpoll_reg_type(mod_point_type)
        mod_data_type = self._modpoll_data_type(mod_data_type)
        if ping:
            command = "timeout 10 modpoll -m rtu -p none -b 9600 -a 1 -t 4:float -r 1  -l 2000 /dev/ttyRS485-1 "
            # if mod_data_type == "raw":
            #     command = f"timeout {mod_run_for} modpoll -m rtu -p none -b {mod_baud_rate}" \
            #               f"-a {mod_device_address} -t {mod_point_type} " \
            #               f"-r {mod_point_address} -c{mod_length} -l {mod_delay} /dev/{mod_serial_port} "
            #
            # else:
            #     command = f"timeout {mod_run_for} modpoll -m rtu -p none -b {mod_baud_rate}" \
            #               f" -a {mod_device_address} -t {mod_point_type}:{mod_data_type}" \
            #               f" -r {mod_point_address}  -l {mod_delay} /dev/{mod_serial_port} "
            logging.info(f"------ MODPOLL ------")
            logging.info(f"------ command: {command} ------")
            host = '192.168.15.10'
            port = 22
            user = 'pi'
            password = 'N00BRCRC'
            # exe = task_command_blank(cx, command)
            ctx = Connection(host=host, port=port, user=user, connect_timeout=3, connect_kwargs={'password': password})
            exe = ctx.run("pwd")
            msg = f"install completed"
            logging.info(exe)
            return msg
        else:
            msg = f"device on ip: {mod_serial_port} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            return msg

    def _reboot_rubix(self):
        cx = self._connection()
        ip = self.parent.setting_remote_update_host.text()
        ping = Utils.ping(ip)
        if ping:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            logging.info("------ Connect and start updates ------")
            reboot_host(cx)
            msg = f"install completed"
            logging.info(msg)
            return msg
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            return msg

    def _update_rubix_service(self):
        cx = self._connection()
        use_config = self.parent.use_config_file.isChecked()
        if use_config:
            ip = _host_settings.get('get_host')
            port = _host_settings.get('get_port')
            user = _host_settings.get('get_user')
            password = _host_settings.get('get_password')
            rubix_username = _bios_settings.get('get_rubix_bios_user')
            rubix_password = _bios_settings.get('get_rubix_bios_password')
            rubix_bios_port = _bios_settings.get('get_rubix_bios_port')
            rubix_service_port = _rubix_settings.get('get_rubix_service_port')
            github_token = _host_settings.get('get_git_token')

        else:
            ip = self.parent.setting_remote_update_host.text()
            rubix_username = self.parent.rubix_username.text()
            rubix_password = self.parent.rubix_password.text()
            rubix_bios_port = self.parent.rubix_bios_port.text()
            rubix_service_port = self.parent.rubix_service_port.text()
            github_token = _host_settings.get('get_git_token')
        ping = Utils.ping(ip)
        githubdl.dl_dir(RUBIX_IMAGE_REPO, RUBIX_SERVICE_CONFIG,
                        github_token=github_token)
        file = f"{CWD}/{RUBIX_SERVICE_CONFIG}/rubix-apps/app.json"
        exe = SSHConnection.run_sftp(cx, file, RUBIX_SERVICE_DIR)
        logging.info(exe)
        if ping:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            logging.info("------ Connect and start updates ------")
            deploy_rubix_service_update(cx,
                                        host=ip,
                                        github_token=github_token,
                                        rubix_username=rubix_username,
                                        rubix_password=rubix_password,
                                        rubix_bios_port=rubix_bios_port,
                                        rubix_service_port=rubix_service_port
                                        )
            msg = f"install completed"
            logging.info(msg)
            return msg
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            return msg

    def check_bbb_connection(self):
        cx = self._connection_bbb()
        if not cx:
            self.parent.run_update_bbb_ip.setEnabled(False)
        else:
            self.parent.run_update_bbb_ip.setEnabled(True)

    def run_update_bbb_ip(self):
        cx = self._connection_bbb()
        bbb_new_ip = self.parent.bbb_new_ip.text()
        bbb_new_mask = self.parent.bbb_new_mask.text()
        bbb_new_router = self.parent.bbb_new_router.text()

        sudo_pass = Responder(
            pattern=r'\[sudo\] password for debian:',
            response='N00B2828\n',
        )

        # exe = cx.run()
        exe = SSHConnection.run_command(cx, LinuxCommands.command_blank("connmanctl services"))
        iface = ''.join(exe.split())[8:]
        new_ip = f"sudo connmanctl config {iface} --ipv4 manual {bbb_new_ip} {bbb_new_mask} {bbb_new_router} --nameservers 8.8.8.8"
        cx.run(new_ip, pty=True, watchers=[sudo_pass])
        new_ip = "sudo pwd"
        cx.run(new_ip, pty=True, watchers=[sudo_pass])

    def bbb_send_env(self):
        cx = self._connection_bbb()
        action = self.parent.bbb_env_option.currentText()
        file = f"{CWD}/.env"
        directory = WIRES_DATA_DIR
        if action == "RESTART_WIRES":
            sudo_pass = Responder(
                pattern=r'\[sudo\] password for debian:',
                response='N00B2828\n',
            )
            cx.run('sudo systemctl restart nubeio-rubix-wires.service', pty=True, watchers=[sudo_pass])
        elif action == "RESTART_HOST":
            sudo_pass = Responder(
                pattern=r'\[sudo\] password for debian:',
                response='N00B2828\n',
            )
            cx.run('sudo reboot', pty=True, watchers=[sudo_pass])
        elif action == "TRANSFER":
            bbb_env_transfer(cx, file, directory)
        elif action == "DELETE":
            sudo_pass = Responder(
                pattern=r'\[sudo\] password for debian:',
                response='N00B2828\n',
            )
            cx.run('sudo rm /data/rubix-wires/config/.env', pty=True, watchers=[sudo_pass])
        elif action == "INSTALL_WIRES":
            sudo_pass = Responder(
                pattern=r'\[sudo\] password for debian:',
                response='N00B2828\n',
            )
            cx.run(
                'wget https://github.com/NubeIO/wires-builds/archive/refs/tags/v2.1.8.zip  && unzip v2.1.8.zip && mv wires-builds-2.1.8 wires-builds && cd wires-builds/rubix-wires/systemd && sudo bash script.bash install -s=nubeio-rubix-wires.service -u=debian --working-dir=/home/debian/wires-builds/rubix-wires -g=/data/rubix-wires -d=data -c=config -p=1313',
                pty=True, watchers=[sudo_pass])

    def _clear_console(self):
        print("ADD LATER")

    def _time_stamp(self):
        dt = datetime.now()
        time = dt.strftime("%d-%b-%Y (%H:%M:%S)")
        return time

    def _ping_host(self):
        ip = self.parent.setting_remote_update_host.text()
        cx = self._connection_status()
        time = self._time_stamp()
        if not cx:
            msg = f"device on ip: {ip} is DEAD {time}"
            logging.info(msg)
        else:
            exe = command_ls(cx)
            if "ERROR" in exe:
                msg = f"device on ip: {ip} is DEAD {time}"
                self.parent.statusBar.showMessage(msg)
            else:
                msg = f"device on ip: {ip} is connected {time}"
                self.parent.statusBar.showMessage(msg)

    def _update_options(self):
        op = self.parent.setting_remote_update_type.currentText()
        op_service = "install rubix service"
        op_service_bios = "install bios & rubix service"
        if op == op_service:
            print(op)
        elif op == op_service_bios:
            print(op)
