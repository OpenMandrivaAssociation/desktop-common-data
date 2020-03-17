%define _build_pkgcheck_set %{nil}
%global __requires_exclude /usr/bin/perl|perl\\(.*\\)

Summary:	Desktop common files
Name:		desktop-common-data
Epoch:		1
Version:	4.1
Release:	1
License:	GPLv2+
URL:		%{disturl}
Group:		System/Configuration/Other

# LATEST SOURCE https://github.com/OpenMandrivaSoftware/desktop-common-data
Source0:	https://github.com/OpenMandrivaSoftware/desktop-common-data/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	libxml2-utils
BuildArch:	noarch
#XDG stuff
Requires:	libxdg-basedir
Requires:	xdg-compliance
Requires:	xdg-user-dirs
Requires:	xdg-utils
Requires:	run-parts
Requires(post):	hicolor-icon-theme
Requires:	hicolor-icon-theme
Conflicts:	kdelibs-common < 30000000:3.5.2
Conflicts:	kdebase-kdm-config-file < 1:3.2-62mdk
Requires(post):	etcskel
Requires(post):	run-parts
Requires:	shared-mime-info
Obsoletes:	menu-messages
%rename		mandrake_desk
%rename		menu
%rename		menu-xdg
%rename	faces-openmandriva
%rename faces-icons

%description
This package contains useful icons, menu structure and others goodies for the
%{distribution} desktop.

%prep
%setup -q

%build
#make

%install
## Install backgrounds
# User & root's backgrounds
install -d -m 0755 %{buildroot}%{_datadir}/mdk/backgrounds/

# for easy access for users looking for wallpapers at expected location
install -d %{buildroot}%{_datadir}/wallpapers
ln -sr %{buildroot}%{_datadir}/mdk/backgrounds %{buildroot}%{_datadir}/wallpapers/mdk

## Install scripts
# /usr/bin/
install -d -m 0755 %{buildroot}/%{_bindir}/
install -m 0755 bin/editor %{buildroot}/%{_bindir}/
install -m 0755 bin/www-browser %{buildroot}/%{_bindir}/
install -m 0755 bin/xvt %{buildroot}/%{_bindir}/

## Install faces
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/faces/
install -d -m 0755 %{buildroot}/%{_datadir}/faces/
cp -a faces/*.png %{buildroot}/%{_datadir}/mdk/faces/

# David - 9.0-5mdk - For KDE
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/default.png

# David - 9.0-5mdk - For GDM
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/user-default-mdk.png

# (tpg) default desktop files (do not place them in /etc/skel/Desktop !)
install -d -m 0755 %{buildroot}%{_datadir}/applications
install -m 0644 desktop/*.desktop %{buildroot}%{_datadir}/applications

#install theme for GDM/KDM
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/dm
for i in dm/*.png dm/*.desktop dm/*.xml ; do
  install -m 0644 $i %{buildroot}/%{_datadir}/mdk/dm/
done

# install bookmarks
install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
for i in bookmarks/konqueror/*.html ; do
  install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
done

install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
for i in bookmarks/mozilla/*.html ; do
  install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
done

mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/kde-applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/gnome-applications.menu

%files
%{_bindir}/*
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/xdg/menus
%config(noreplace) %{_sysconfdir}/xdg/menus/*.menu
%dir %{_datadir}/faces/
%{_datadir}/faces/default.png
%{_datadir}/faces/user-default-mdk.png
%dir %{_datadir}/mdk/
%dir %{_datadir}/mdk/faces/
%{_datadir}/mdk/faces/*.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/mdk/backgrounds
%{_datadir}/wallpapers/mdk
%dir %{_datadir}/mdk/bookmarks
%dir %{_datadir}/mdk/bookmarks/konqueror
%{_datadir}/mdk/bookmarks/konqueror/*.html
%dir %{_datadir}/mdk/bookmarks/mozilla
%{_datadir}/mdk/bookmarks/mozilla/*.html
%{_datadir}/mdk/dm
