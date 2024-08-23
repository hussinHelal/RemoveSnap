sudo snap list // list snap and remove it like commands bellow

sudo snap remove --purge firefox
sudo snap remove --purge snap-store
sudo snap remove --purge gnome-3-38-2004
sudo snap remove --purge gtk-common-themes
sudo snap remove --purge snapd-desktop-integration
sudo snap remove --purge bare
sudo snap remove --purge core22
sudo snap remove --purge snapd
sudo apt --autoremove snapd 

sudo vim /etc/apt/preferences.d/nosnap.pref // and put this inside

Package: snapd
Pin: release a=*
Pin-Priority: -10

=== 

sudo apt update 

sudo apt install --install-suggests gnome-software

sudo add-apt-repository ppa:mozillateam/ppa
sudo apt update
sudo apt install -t 'o=LP-PPA-mozillateam' firefox

echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox


sudo vim /etc/apt/preferences.d/mozillateamppa

Package: firefox*
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 501


====


// and that's it

