import getpass
import shutil
import os
import subprocess
from sys import argv
import json
import sys
# from git import Repo


# TODO: Move Background image to /usr/local/share/background
# TODO: Install Teamviewer from aur
# TODO: Install Citrix from aur
# TODO: Install plymouth
# TODO: Autorun teamviewer
# TODO: var/lib/acc...
# with open("hello.txt") as my_file:
#     for line in my_file:
#         print(line)


# Directories
users = ['mitarbeiter', 'admin']
home_dir = '/home/'
temp_dwn_dir = '/tmp/setup/'


# TODO: Install packages
def install_pkgs():
    for pkg in json.loads('./data/pgks.json'):
        subprocess.run(['pacman', '-S', pkg, '--noconfirm'],
                       capture_output=True)


# TODO: Edit environment variables -> ~/.config/environent.d/variables.conf
def create_env_var():
    # Check if file for environment variable exists
    # Else create new one
    for u in users:
        print(f'{home_dir}{u}/.config/environment.d/')
        if not os.path.exists(f'{home_dir}{u}/.config/environment.d/'):
            os.makedirs(f'{home_dir}{u}/.config/environment.d/')
        with open(f'{home_dir}{u}/.config/environment.d/variable.conf', 'w') as f:
            f.write(f'DCONF_PROFILE=/etc/dconf/profile/{u}')
        subprocess.run(
            ['chown', '-R', 'root:{u}', f'{home_dir}{u}/.config/environment.d'])
        subprocess.run(
            ['chmod', '-R', '0644', f'{home_dir}{u}/.config/environment.d'])


# TODO: Move dconf-files to /etc/dconf/ -> Update dconf
def setup_dconf():
    if os.path.exists('/etc/dconf'):
        shutil.rmtree('/etc/dconf')
    shutil.copytree(f'{temp_dwn_dir}dconf/',
                    '/etc/dconf')
    subprocess.run(['dconf', 'update'])


# TODO: Load grub.cfg
def load_grub_cfg():
    if os.path.exists('/etc/default/grub'):
        os.remove('/etc/default/grub')
    shutil.copy(f'{temp_dwn_dir}grub', '/etc/default/grub')
    subprocess.run(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'])


# TODO: Move Desktop Applications to ~/.local/applications
def setup_desktop_apps():
    if not os.path.exists(f'{home_dir}.local/share/applications'):
        os.makedirs(f'{home_dir}.local/share/applications')
    for file in os.listdir(f'/usr/share/applications'):
        shutil.copy(f'/usr/share/applications',
                    f'{home_dir}.local/share/applications')
    # copy_tree(f'/usr/share/applications',
    #           f'{user_home_dir}.local/share/applications')

    # TODO: Edit .desktop files | Add "NoDisplay=true" if app should not be shown
    for file in os.listdir(f'{home_dir}.local/share/applications'):
        with open(f'{home_dir}.local/share/applications/{file}', 'r+') as f:
            contents = f.readlines()
            if 'NoDisplay=true' not in contents:
                contents.insert(2, 'NoDisplay=true')
                contents = "".join(contents)
                f.write(contents)
                f.close()


# Create new users
def create_users():
    # Asking for users password
    for u in users:
        password = getpass.getpass()

        try:
            # executing useradd command using subprocess module
            subprocess.run(['useradd', '-p', password, u])
        except:
            print(f"Failed to add user.")
            sys.exit(1)


def copy_xx():
    for u in users:
        pass


# def install_aur():
#     for pkg in ['teamviewer', 'icaclient']:
#         Repo.clone_from(
#             f'https://aur.archlinux.org/{pkg}', admin_home_dir)
#         subprocess.run([f"cd", admin_home_dir, pkg], check=True, text=True)
#         subprocess.run(["sudo -u admin makepkg -si"], check=True, text=True)
#         subprocess.run(["cd"], check=True, text=True)
#         shutil.rmtree(f'{admin_home_dir}{pkg}')
#         # systemctl enable
if __name__ == '__main__':
    create_env_var()
    setup_dconf()
    load_grub_cfg()
    # setup_desktop_apps()

    # shutil.rmtree(temp_dwn_dir)
