import paramiko
import logging


class SSHManage(object):
    def create_ssh_connection(self, host, user, key_filename):
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, 22, username=user, key_filename=key_filename)
            return ssh
        except Exception as e:
            logging.INFO(e)

    def ssh_read_data(self, host, path_file, key_filename, login):
        text = ''
        try:
            ssh_connect = self.create_ssh_connection(host, login, key_filename)
            sftp = ssh_connect.open_sftp()
            with sftp.open('{}'.format(path_file), 'r')as file_edit:
                text_data = file_edit.read()
            text = text_data
            sftp.close()
        except Exception as e:
            logging.INFO(e)
        finally:
            if ssh_connect:
                ssh_connect.close()
        return text


    def ssh_rem_comand(self, host, user, key_filename, command):
        """
            This could restart shorewall via ssh with check (check:'yes') and other services without check service.
            :param host: host
            :param name_service: service of linux(ipsec or shorewall)
            :param check: use 'yes' for check shorewall
            :return: None
            #/usr/bin/fetchmail -k
        """
        try:
            ssh_connect = self.create_ssh_connection(host, user, key_filename)
            stdin, stdout, stderr = ssh_connect.exec_command('{}'.format(command))
            print(stdout.readlines())
        except Exception as e:
            print(e)
        finally:
            if ssh_connect:
                ssh_connect.close()