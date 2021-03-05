import paramiko
import time
import getpass

host = "intuition.thayer.dartmouth.edu"
port = 22
#username = "****"
#password = "****"



# python3.8 runRoMDP.py "TTR_auto/16.02.2021_15.34.17/target" "TTR_auto/16.02.2021_15.34.17/other" "" "" 100 BARON "TTR_auto/16.02.2021_15.34.17/output"
class ssh:
    def __init__(self, folder, loops, player1Strat, player2Strat, features):
        username = input("Enter intuition username: ")
        password = getpass.getpass("Enter intuition password: ")
        self.folder = folder
        self.loops = loops
        feat = 'ex' if features == 'extended' else 'lim'


        target = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/target/'.format(username, folder, features)
        other = '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/{}/other/'.format(username, folder, features)

        filename = 'output_CSVs/{}/{}/target/list.files'.format(folder, features)
        f = open(filename, 'w')
        filename1 = 'output_CSVs/{}/{}/other/list.files'.format(folder, features)
        f1 = open(filename1, 'w')
        for x in range(1, loops+1):
            f.write('TTR_auto/{}/{}/target/{}_{}_{}.csv\n'.format(folder, features, player1Strat, feat, x))
            f1.write('TTR_auto/{}/{}/other/{}_{}_{}.csv\n'.format(folder, features, player2Strat, feat, x))
        f.close()
        f1.close()

        server_ssh = paramiko.SSHClient()
        server_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        server_ssh.connect(host, port, username, password)

        stdin, stdout, stderr = server_ssh.exec_command("/admin/clust report c")

        for line in stdout.readlines()[1:]:
            line = line.split()
            if len(line) == 8:
                node_name = line[0]
                break

        transport = server_ssh.get_transport()
        node_dest = (node_name, port)
        server_dest = (host, port)
        tunnel = transport.open_channel('direct-tcpip', node_dest, server_dest)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(node_name, username=username, password=password, sock=tunnel)

        sftp = ssh.open_sftp()

        cdms = ['cd src/C++/DTM/ToyDTMs/TTR_auto', 'mkdir {}'.format(folder), 'cd {}'.format(folder),
                'mkdir {}'.format(features), 'cd {}'.format(features), 'mkdir {}'.format('target'), 'mkdir {}'.format('other')]
        print(str(cdms))
        stdin, stdout, stderr = ssh.exec_command(';'.join(cdms))
        print('Made ' + str(folder) + ' folder inside TTR_auto')

        sftp.put(
            'dtmFiles/actions.csv',
            target + '/actions.csv')
        sftp.put(
            'dtmFiles/actions.csv',
            other + '/actions.csv')

        sftp.put(
            'dtmFiles/{}/attributes.csv'.format(feat),
            target + '/attributes.csv')
        sftp.put(
            'dtmFiles/{}/attributes.csv'.format(feat),
            other + '/attributes.csv')

        sftp.put(
            'output_CSVs/{}/{}/target/list.files'.format(folder, features),
            target + '/list.files')
        sftp.put(
            'output_CSVs/{}/{}/other/list.files'.format(folder, features),
            other + '/list.files')

        for x in range(1, loops + 1):
            sftp.put(
                'output_CSVs/{}/{}_{}_{}.csv'.format(folder, player1Strat, feat, x),
                target + '/{}_{}_{}.csv'.format(player1Strat, feat, x))
            sftp.put(
                'output_CSVs/{}/{}_{}_{}.csv'.format(folder, player2Strat, feat, x),
                other + '/{}_{}_{}.csv'.format(player2Strat, feat, x))

        sftp.close()

        cdms = ['cd src/C++/DTM/ToyDTMs/', 'python3.8 runRoMDP.py "TTR_auto/{}/{}/target" "TTR_auto/{}/{}/other" "" "" 100 BARON "TTR_auto/{}/{}/output"'.format(folder, features, folder, features, folder, features)]
        print(cdms[1])
        ssh.exec_command(';'.join(cdms))
        time.sleep(5)

        # cdms = ['cd src/C++/DTM/ToyDTMs/',
        #        'python3.8 runRoMDP.py "TTR_auto/18.02.2021_14.16.42/target" "TTR_auto/18.02.2021_14.16.42/other" "" "" 100 BARON "TTR_auto/18.02.2021_14.16.42/output"']

        #cdms = ['ssh {}'.format(node_name)]
        #ssh.exec_command(';'.join(cdms))
        #cdms = ['cd src/C++/DTM/ToyDTMs/', 'python3.8 runRoMDP.py \"TTR_auto/{}/target\" \"TTR_auto/{}/other\" \"\" \"\" 100 BARON \"TTR_auto/{}/output\"'.format(folder, folder, folder)]
        #ssh.exec_command(';'.join(cdms))

        #cdms = ['ssh {}'.format(node_name), 'cd src/C++/DTM/ToyDTMs/', 'python3.8 runRoMDP.py "TTR_auto/16.02.2021_15.51.38/target" "TTR_auto/16.02.2021_15.51.38/other" "" "" 100 BARON "TTR_auto/16.02.2021_15.51.38/output"']
        #print(str(cdms))
        #stdin, stdout, stderr = ssh.exec_command(';'.join(cdms))



        #sftp.get(
        #    '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/16.02.2021_16.57.46/output-BARON/RoMDP-BARON.graphml.gz'.format(username),
        #    'output_CSVs/16.02.2021_16.57.46/output-BARON/RoMDP-BARON.graphml.gz')
        #sftp.get(
        #    '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/{}/output-RoMDP-BARON'.format(username, folder),
        #    'output_CSVs/{}/output-RoMDP-BARON').format(folder)

        #sftp.get(
        #    '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/16.02.2021_16.32.02/output-BARON'.format(username),
        #    'output_CSVs/16.02.2021_16.32.02/output-BARON')
        #sftp.get(
        #    '/home/{}/src/C++/DTM/ToyDTMs/TTR_auto/16.02.2021_16.32.02/output-RoMDP-BARON'.format(username),
        #    'output_CSVs/16.02.2021_16.32.02/output-RoMDP-BARON')

        sftp.close()
        ssh.close()
        server_ssh.close()

        #14511110
        '''
        1131111000
        '''
        #/src/C++/DTM/ToyDTMs/TTR_auto
        #python3.8 runRoMDP.py "TTR_auto/18.02.2021_14.16.42/target" "TTR_auto/18.02.2021_14.16.42/other" "" "" 100 BARON "TTR_auto/18.02.2021_14.16.42/output"