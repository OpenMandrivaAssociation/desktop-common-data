Summary:	Desktop common files
Name:		desktop-common-data
Version:	2013.0
Release:	7
License:	GPLv2+
URL:		http://www.mandriva.com/
Group:		System/Configuration/Other

# get the source from our svn repository (svn+ssh://svn.mandriva.com/svn/soft/desktop-common-data/)
# no extra source or patch are allowed here.
# to generate this tarball, from svn repository above, 
# run "make dist VERSION=%{version} RELEASE=xxmdk"
# where xx is version used for mkrel
Source0:	%{name}-%{version}.tar.xz
Patch0:		desktop-common-data-2011.0-menu.patch

BuildRequires:	intltool
BuildRequires:	menu-messages
BuildRequires:	gettext
BuildRequires:	libxml2-utils
BuildArch:	noarch
Obsoletes:	mandrake_desk < %{version}
Provides:	mandrake_desk
Conflicts:	kdebase-kdm-config-file < 1:3.2-62mdk
Obsoletes:	menu < %{version}
Obsoletes:	menu-xdg  < %{version}
Provides:	menu-xdg
Provides:	menu = 2.1.24
Requires:	menu-messages
Requires:	xdg-utils
Requires:	xdg-user-dirs
Requires:	run-parts
Requires(post):	hicolor-icon-theme
Requires:	hicolor-icon-theme
Conflicts:	kdelibs-common < 30000000:3.5.2
Requires:	faces-icons

%description
This package contains useful icons, menu structure and others goodies for the
%{distribution} desktop.

%package -n	faces-moondrake
Summary:	Original classic cute penguins by Helene Durosini, rescaled by Anette Norli
Url:		http://www.anettenorli.com
Group:		System/Configuration/Other
Provides:	faces-icons
Requires(post):	update-alternatives
Requires(postun):update-alternatives

%description -n	faces-moondrake
Penguin faces from previous Mandriva Linux releases, originally drawn by
Helene Durosini, rescaled and enhanced by Anette Norli.

%package -n	faces-default
Summary:	Default set of face icons from Mandriva Linux 2011
Group:		System/Configuration/Other
Provides:	faces-icons
Requires(post):	update-alternatives
Requires(postun):update-alternatives

%description -n	faces-default
Default set of face icons that were used in Mandriva Linux 2011.

%prep
%setup -q
%patch0 -p1

%build
make

%install
## Install backgrounds
# User & root's backgrounds
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/backgrounds/
install -m644 backgrounds/default.png %{buildroot}/%{_datadir}/mdk/backgrounds/
install -m 0644 backgrounds/flower.jpg %{buildroot}/%{_datadir}/mdk/backgrounds/
install -m 0644 backgrounds/nature.jpg %{buildroot}/%{_datadir}/mdk/backgrounds/

# XFdrake test card
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/xfdrake/
install -m 0644 backgrounds/xfdrake-test-card.png %{buildroot}/%{_datadir}/mdk/xfdrake/xfdrake-test-card.png

# for easy access for users looking for wallpapers at expected location
install -d %{buildroot}%{_datadir}/wallpapers
ln -sr %{buildroot}%{_datadir}/mdk/backgrounds %{buildroot}%{_datadir}/wallpapers/mdk

## Install scripts
# /usr/bin/
install -d -m 0755 %{buildroot}/%{_bindir}/
for i in bin/*.sh ; do install -m 0755 $i %{buildroot}/%{_bindir}/ ; done
install -m 0755 bin/www-browser %{buildroot}/%{_bindir}/
install -m 0755 bin/xvt %{buildroot}/%{_bindir}/

# /usr/sbin/
install -d -m 0755 %{buildroot}/%{_sbindir}/
for i in sbin/* ; do install -m 0755 $i %{buildroot}/%{_sbindir}/ ; done


## Install faces
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/faces/
install -d -m 0755 %{buildroot}/%{_datadir}/faces/
cp -a faces/*/ %{buildroot}/%{_datadir}/mdk/faces/

# David - 9.0-5mdk - For KDE
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/default.png

# David - 9.0-5mdk - For GDM
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/user-default-mdk.png

## KDE
# kdm
install -d -m 0755 %{buildroot}/%{_datadir}/apps/kdm/pics/
install -m 0644 kde/kdm-mdk-logo.png %{buildroot}/%{_datadir}/apps/kdm/pics/



## icons
install -d -m 0755 %{buildroot}/%{_miconsdir} %{buildroot}/%{_liconsdir}
install -m 0644 menu/icons/*.png %{buildroot}/%{_iconsdir}
install -m 0644 menu/icons/large/*.png %{buildroot}/%{_liconsdir}
install -m 0644 menu/icons/mini/*.png %{buildroot}/%{_miconsdir}
cp -r menu/icons/hicolor  %{buildroot}/%{_datadir}/icons/

# XDG menus
install -d -m 0755 %{buildroot}/%{_sysconfdir}/xdg/autostart
install -d -m 0755 %{buildroot}/%{_sysconfdir}/xdg/menus/applications-merged
install -d -m 0755 %{buildroot}/%{_sysconfdir}/menu.d %{buildroot}/%{_sysconfdir}/profile.d
install -m 0644 applications.menu %{buildroot}/%{_sysconfdir}/xdg/menus/applications.menu
install -m 0644 kde-applications.menu %{buildroot}/%{_sysconfdir}/xdg/menus/kde-applications.menu
install -m 0755 menu/xdg_menu %{buildroot}/%{_bindir}
install -m 0755 menu/update-menus %{buildroot}/%{_bindir}/update-menus
install -m 0644 menu/menustyle.csh %{buildroot}/%{_sysconfdir}/profile.d/30menustyle.csh
install -m 0644 menu/menustyle.sh  %{buildroot}/%{_sysconfdir}/profile.d/30menustyle.sh

if [ "%_install_langs" != "all" ]; then
 echo ERROR : rpm macro %%_install_langs is not set to \"all\", causing some translations to not be available on your build system and therefore preventing building this package. Add \"%%_install_langs all\" to /etc/rpm/macros and force a reinstall of mdk-menu-messages package to ensure all translations are installed on this system before rebuilding this package
 return 1
fi

install -d -m 0755 %{buildroot}/%{_datadir}/desktop-directories
mkdir -p tmp-l10n
for i in %{_datadir}/locale/*/LC_MESSAGES/menu-messages.mo ; do
 msgunfmt $i > tmp-l10n/`echo $i | sed -e 's|%{_datadir}/locale/||' -e 's|/LC.*||'`.po
done

install -d -m 0755 %{buildroot}/%{_var}/lib/menu
 
for i in menu/desktop-directories/*.in ; do
 %{_bindir}/intltool-merge --desktop-style -c tmp-l10n/cache tmp-l10n $i %{buildroot}/%{_datadir}/desktop-directories/`basename $i .in` 2>&1 | grep -q "Odd number of elements in hash assignment" && echo "menu message po broken (see bug #25895), aborting " && exit 1
done

#install theme for GDM/KDM
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/dm
for i in dm/*.png dm/*.desktop dm/*.xml ; do 
  install -m 0644 $i %{buildroot}/%{_datadir}/mdk/dm/
done

# install bookmarks
install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
for i in bookmarks/konqueror/*.xml ; do 
  install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
done

install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
for i in bookmarks/mozilla/*.html ; do 
  install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
done

# install sound samples
install -d -m 0755 %{buildroot}%{_datadir}/sounds
cp -r sounds/moondrake %{buildroot}%{_datadir}/sounds

#install sound theme Ia Ora
cp -r sounds/ia_ora %{buildroot}%{_datadir}/sounds
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/dialog.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/power.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/battery.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/suspend.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/screen-capture.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/service.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/system.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/desktop.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/device.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/bell.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/message-new-email.disabled
touch  %{buildroot}%{_datadir}/sounds/ia_ora/stereo/trash-empty.disabled


%post
if [ -f %{_sysconfdir}/X11/window-managers.rpmsave ];then
	%{_sbindir}/convertsession -f %{_sysconfdir}/X11/window-managers.rpmsave || :
fi
%make_session
# (cg) See sound-theme-freedesktop for explanation about touch.
touch --no-create %{_datadir}/sounds %{_datadir}/sounds/ia_ora

%postun
# (cg) See sound-theme-freedesktop for explanation about touch.
touch --no-create %{_datadir}/sounds %{_datadir}/sounds/ia_ora

%triggerin -- %{_datadir}/applications/*.desktop, %{_datadir}/applications/*/*.desktop
%{_bindir}/update-menus

%triggerin -- %{_datadir}/X11/dm.d/*.conf, %{_sysconfdir}/X11/wmsession.d/*
%{_sbindir}/fndSession

%triggerpostun -- %{_datadir}/applications/*.desktop, %{_datadir}/applications/*/*.desktop
%{_bindir}/update-menus

%triggerpostun -- %{_datadir}/X11/dm.d/*.conf, %{_sysconfdir}/X11/wmsession.d/*
%{_sbindir}/fndSession

%post -n faces-moondrake
update-alternatives --install %{_datadir}/mdk/faces/default.png default-faces.png %{_datadir}/mdk/faces/00-moondrake/plaintux.png 10

%postun -n faces-moondrake
if [ "$1" = "0" ]; then
  update-alternatives --remove default-faces.png %{_datadir}/mdk/faces/00-moondrake/plaintux.png
fi

%post -n faces-default
update-alternatives --install %{_datadir}/mdk/faces/default.png default-faces.png %{_datadir}/mdk/faces/02-default/default.png 1

%postun -n faces-default
if [ "$1" = "0" ]; then
  update-alternatives --remove default-faces.png %{_datadir}/mdk/faces/02-default/default.png
fi

%files
%{_bindir}/*
#
%{_sbindir}/*

%{_sysconfdir}/profile.d/*
%dir %{_sysconfdir}/menu.d
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/xdg/menus
%dir %{_sysconfdir}/xdg/menus/applications-merged
%config(noreplace) %{_sysconfdir}/xdg/menus/*.menu
%dir %{_var}/lib/menu

#
%dir %{_datadir}/faces/
%dir %{_datadir}/mdk/
%dir %{_datadir}/mdk/faces/
%{_datadir}/faces/*
#
%dir %{_datadir}/mdk/backgrounds/
%{_datadir}/mdk/backgrounds/*.jpg
%{_datadir}/mdk/backgrounds/default.png

%{_datadir}/wallpapers/mdk


%dir %{_datadir}/mdk/bookmarks
%dir %{_datadir}/mdk/bookmarks/konqueror
%{_datadir}/mdk/bookmarks/konqueror/*.xml
%dir %{_datadir}/mdk/bookmarks/mozilla
%{_datadir}/mdk/bookmarks/mozilla/*.html
#
%dir %{_datadir}/apps/kdm/pics/
%{_datadir}/apps/kdm/pics/*
#
%dir %{_datadir}/mdk/xfdrake/
%{_datadir}/mdk/xfdrake/*.png
#

%{_datadir}/sounds/ia_ora
%{_datadir}/sounds/moondrake

%{_datadir}/mdk/dm
#
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/desktop-directories/*.directory

%files -n faces-moondrake
%dir %{_datadir}/mdk/faces/00-moondrake
%{_datadir}/mdk/faces/00-moondrake/*

%files -n faces-default
%dir %{_datadir}/mdk/faces/02-default
%{_datadir}/mdk/faces/02-default/*
