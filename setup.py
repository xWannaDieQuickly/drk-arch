import shutil
import os


# TODO: Move Background image to /usr/local/share/background
# TODO: Install Teamviewer from aur
# TODO: Install Citrix from aur
# TODO: Install plymouth


# Directories
user_home_dir = '/home/mitarbeiter/'

# TODO: Edit environment variables -> ~/.config/environent.d/variables.conf


def create_env_var():
    # Check if file for environment variable exists
    # Else create new one
    if not os.path.exists(f'{user_home_dir}.config/environment.d/variable.conf'):
        os.mkdir(f'{user_home_dir}.config/environment.d/')
        with open('variable.conf', 'w') as f:
            f.write('DCONF_PROFILE="/etc/dconf/profile/mitarbeiter"')
            f.close()


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


# TODO: Move dconf-files to /etc/dconf/ -> Update dconf
def setup_dconf():
    shutil.rmtree('/etc/dconf')
    shutil.copytree('dconf', 'etc/')
    print()


def main():
    create_env_var()
    setup_dconf()
    setup_desktop_apps()


main()
