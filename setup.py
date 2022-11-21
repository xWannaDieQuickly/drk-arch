import shutil
import os
import subprocess
# from git import Repo


# TODO: Move Background image to /usr/local/share/background
# TODO: Install Teamviewer from aur
# TODO: Install Citrix from aur
# TODO: Install plymouth
# TODO: Autorun teamviewer


# Directories
user_home_dir = '/home/mitarbeiter/'
admin_home_dir = '/home/admin/'
temp_dwn_dir = '/temp/setup/'
github = 'https://www.github.com/xannadiequickly/backup'


# TODO: Edit environment variables -> ~/.config/environent.d/variables.conf
def create_env_var():
    # Check if file for environment variable exists
    # Else create new one
    if os.path.exists(f'{user_home_dir}.config/environment.d'):
        shutil.rmtree(f'{user_home_dir}.config/environment.d')

    os.makedirs(f'{user_home_dir}.config/environment.d')
    shutil.copy(f'{temp_dwn_dir}environment.d/variable.conf',
                f'{user_home_dir}.config/environment.d/')

# TODO: Move dconf-files to /etc/dconf/ -> Update dconf


def setup_dconf():
    if os.path.exists('/etc/dconf'):
        shutil.rmtree('/etc/dconf')
        return

    os.makedirs('/etc/dconf/db/mitarbeiter.d/locks')
    os.makedirs('/etc/dconf/profile')
    shutil.copy(f'{temp_dwn_dir}dconf/db/mitarbeiter.d/locks/01-background',
                '/etc/dconf/db/mitarbeiter.d/locks/')
    shutil.copy(f'{temp_dwn_dir}dconf/db/mitarbeiter.d/01-background',
                '/etc/dconf/db/mitarbeiter.d')
    shutil.copy(f'{temp_dwn_dir}dconf/db/mitarbeiter.d/00-lockdown',
                '/etc/dconf/db/mitarbeiter.d')
    shutil.copy(f'{temp_dwn_dir}dconf/profile/mitarbeiter',
                '/etc/dconf/profile')


# TODO: Load grub.cfg
def load_grub_cfg():
    if not os.path.exists('/etc/default/grub'):
        os.mkdir('/etc/default/grub')
        shutil.copyfile(f'{temp_dwn_dir}grub', '/etc/default/grub')


# TODO: Move Desktop Applications to ~/.local/applications
def setup_desktop_apps():
    if not os.path.exists(f'{user_home_dir}.local/share/applications'):
        os.mkdir(f'{user_home_dir}.local/share/applications')
    if len(os.listdir(f'{user_home_dir}.local/share/applications')) == 0:
        shutil.copytree('/usr/share/applications',
                        f'{user_home_dir}.local/share/applications')

    # TODO: Edit .desktop files | Add "NoDisplay=true" if app should not be shown
    for file in os.listdir(f'{user_home_dir}.local/share/applications'):
        with open(f'{user_home_dir}.local/share/applications/{file}', 'r+') as f:
            contents = f.readlines()
            if 'NoDisplay=true' not in contents:
                contents.insert(2, 'NoDisplay=true')
                contents = "".join(contents)
                f.write(contents)
                f.close()


# def install_aur():
#     for pkg in ['teamviewer', 'icaclient']:
#         Repo.clone_from(
#             f'https://aur.archlinux.org/{pkg}', admin_home_dir)
#         subprocess.run([f"cd", admin_home_dir, pkg], check=True, text=True)
#         subprocess.run(["sudo -u admin makepkg -si"], check=True, text=True)
#         subprocess.run(["cd"], check=True, text=True)
#         shutil.rmtree(f'{admin_home_dir}{pkg}')
#         # systemctl enable


def main():
    # os.mkdir('(/temp/setup')
    # Repo.clone_from(
    #     github, temp_dwn_dir)
    create_env_var()
    setup_dconf()
    load_grub_cfg()
    # setup_desktop_apps()

# sudo -u admin [cmd]


main()
