dnf rm abrt avahi audit adobe-mappings-cmap ; 
dnf rm containernetworking-plugins cups cups-client empathy evolution evince fedora-workstation-backgrounds f31-backgrounds-base flatpak foomatic-db-ppds fpaste;
dnf rm geolite2-city gnome-classic-session gnome-contacts gnome-getting-started-docs  gnome-user-docs gnome-tour gssproxy gutenprint gvfs-gphoto2 gucharmap iok 'hplip*' 'kde*' libpurple libreoffice-emailmerge libreoffice-math;
dnf rm libreport;
dnf rm m17n-contrib mcelog  'qemu*' qt-x11 orca ;
dnf rm open-vm-tools pcsc-lite pcsc-lite-libs php-common redis rhythmbox rng-tools samba-client sane-backends sane-backends-libs shotwell 'selinux-policy*' sssd 'libsss_*' totem tracker-miners;
dnf rm virtualbox-guest-additions vim-filesystem vim-minimal yum;
# i18n
dnf rm libpinyin libkkc libkkc-data libhangul opencc   thai-scalable-fonts-common   nhn-nanum-gothic-fonts wqy-zenhei-fonts smc-fonts-common    smc-meera-fonts skkdic cjkuni-uming-fonts;
dnf rm PackageKit;
DISABLE_SERVICES="atd dnf-makecache mdmonitor NetworkManager-wait-online redis unbound-anchor.timer"; for i in $DISABLE_SERVICES; do systemctl stop $i;  systemctl disable $i; done
