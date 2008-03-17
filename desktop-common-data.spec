Summary:	Desktop common files 
Name:		desktop-common-data
Version:	2008.1
Release: 	%mkrel 7
License:	GPL
URL:		http://www.mandrivalinux.com/
Group:		System/Configuration/Other

# get the source from our svn repository (svn+ssh://svn.mandriva.com/svn/soft/desktop-common-data/)
# no extra source or patch are allowed here.
# to generate this tarball, from svn repository above, 
# run "make dist VERSION=%{version} RELEASE=xxmdk"
# where xx is version used for mkrel
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	intltool
%if %mdkversion >= 200810
BuildRequires:  menu-messages
%else
BuildRequires:	mdk-menu-messages
%endif
BuildRequires:  gettext
BuildRequires:  libxml2-utils
BuildArch:	noarch
Obsoletes:	mandrake_desk
Provides:	mandrake_desk
Conflicts:	kdebase-kdm-config-file < 1:3.2-62mdk
Obsoletes:	menu
Obsoletes:	menu-xdg
Provides:	menu-xdg
Provides:	menu = 2.1.24
%if %mdkversion >= 200810
Requires:	menu-messages 
%else
Requires:	mdk-menu-messages 
%endif
Requires:	xdg-utils
Requires:	xdg-user-dirs
Requires(post):	hicolor-icon-theme
Requires:	hicolor-icon-theme
Conflicts:      kdelibs-common < 30000000:3.5.2

%description
This package contains useful icons, menu structure and others goodies for the
Mandriva Linux desktop.

%prep
%setup -q

%build

make


%install
rm -rf %buildroot

## Install backgrounds
# User & root's backgrounds
install -d -m 0755 %buildroot/%_datadir/mdk/backgrounds/
install -m 0644 backgrounds/flower.jpg %buildroot/%_datadir/mdk/backgrounds/
install -m 0644 backgrounds/nature.jpg %buildroot/%_datadir/mdk/backgrounds/

# XFdrake test card
install -d -m 0755 %buildroot/%_datadir/mdk/xfdrake/
install -m 0644 backgrounds/xfdrake-test-card.png %buildroot/%_datadir/mdk/xfdrake/xfdrake-test-card.png



## Install scripts
# /usr/bin/
install -d -m 0755 %buildroot/%_bindir/
for i in bin/*.sh ; do install -m 0755 $i %buildroot/%_bindir/ ; done
install -m 0755 bin/www-browser %buildroot/%_bindir/
install -m 0755 bin/xvt %buildroot/%_bindir/

# /usr/sbin/
install -d -m 0755 %buildroot/%_sbindir/
for i in sbin/* ; do install -m 0755 $i %buildroot/%_sbindir/ ; done

# /etc/X11/xinit.d/
install -d -m 0755 %buildroot/%_sysconfdir/X11/xinit.d/
for i in xinit.d/* ; do install -m 0755 $i %buildroot/%_sysconfdir/X11/xinit.d/ ; done


## Install faces
install -d -m 0755 %buildroot/%_datadir/mdk/faces/
install -d -m 0755 %buildroot/%_datadir/faces/
for i in faces/*.png ; do install -m 0644 $i %buildroot/%_datadir/mdk/faces/ ; done
		
# David - 9.0-5mdk - For KDE
install -m 0644 faces/default.png %buildroot/%_datadir/faces/default.png

# David - 9.0-5mdk - For GDM
install -m 0644 faces/default.png %buildroot/%_datadir/faces/user-default-mdk.png



## KDE
# kdm
install -d -m 0755 %buildroot/%_datadir/apps/kdm/pics/
install -m 0644 kde/kdm-mdk-logo.png %buildroot/%_datadir/apps/kdm/pics/



## icons
install -d -m 0755 %buildroot/%_miconsdir %buildroot/%_liconsdir
install -m 0644 menu/icons/*.png %buildroot/%_iconsdir
install -m 0644 menu/icons/large/*.png %buildroot/%_liconsdir
install -m 0644 menu/icons/mini/*.png %buildroot/%_miconsdir
cp -r menu/icons/hicolor  %buildroot/%_datadir/icons/

# XDG menus
install -d -m 0755 %buildroot/%_sysconfdir/xdg/menus/applications-merged 
install -d -m 0755 %buildroot/%_sysconfdir/menu.d %buildroot/%_sysconfdir/profile.d
install -m 0644 applications.menu %buildroot/%_sysconfdir/xdg/menus/applications.menu
install -m 0644 kde-applications.menu %buildroot/%_sysconfdir/xdg/menus/kde-applications.menu
install -m 0755 menu/xdg_menu %buildroot/%_bindir
install -m 0755 menu/update-menus %buildroot/%_bindir/update-menus
install -m 0644 menu/menustyle.csh %buildroot/%_sysconfdir/profile.d/30menustyle.csh
install -m 0644 menu/menustyle.sh  %buildroot/%_sysconfdir/profile.d/30menustyle.sh

if [ "%_install_langs" != "all" ]; then
 echo ERROR : rpm macro %%_install_langs is not set to \"all\", causing some translations to not be available on your build system and therefore preventing building this package. Add \"%%_install_langs all\" to /etc/rpm/macros and force a reinstall of mdk-menu-messages package to ensure all translations are installed on this system before rebuilding this package
 return 1
fi

install -d -m 0755 %buildroot/%_datadir/desktop-directories
mkdir tmp-l10n
for i in %_datadir/locale/*/LC_MESSAGES/menu-messages.mo ; do
 msgunfmt $i > tmp-l10n/`echo $i | sed -e 's|%{_datadir}/locale/||' -e 's|/LC.*||'`.po
done

install -d -m 0755 %buildroot/%_var/lib/menu
 
for i in menu/desktop-directories/*.in ; do
 %{_bindir}/intltool-merge --desktop-style -c tmp-l10n/cache tmp-l10n $i %buildroot/%_datadir/desktop-directories/`basename $i .in` 2>&1 | grep -q "Odd number of elements in hash assignment" && echo "menu message po broken (see bug #25895), aborting " && exit 1
done

for PRODUCT in free one powerpack ; do 
  install -d -m 0755 %buildroot/%_datadir/mdk/desktop/$PRODUCT
  for i in desktop/$PRODUCT/*.in ; do
    %{_bindir}/intltool-merge --desktop-style -c tmp-l10n/cache tmp-l10n $i %buildroot/%_datadir/mdk/desktop/$PRODUCT/`basename $i .in` 
  done
done


#install theme for GDM/KDM
install -d -m 0755 %buildroot/%_datadir/mdk/dm
for i in dm/*.png dm/*.desktop dm/*.xml ; do 
  install -m 0644 $i %buildroot/%_datadir/mdk/dm/
done

# install bookmarks
install -d -m 0755 %buildroot%_datadir/mdk/bookmarks/konqueror
for i in bookmarks/konqueror/*.xml ; do 
  install -m 0644 $i %buildroot%_datadir/mdk/bookmarks/konqueror
done

install -d -m 0755 %buildroot%_datadir/mdk/bookmarks/mozilla
for i in bookmarks/mozilla/*.html ; do 
  install -m 0644 $i %buildroot%_datadir/mdk/bookmarks/mozilla
done

# install sound samples
install -d -m 0755 %buildroot%_datadir/sounds
for i in sounds/ia_ora*.wav ; do
 install -m 0644 $i %buildroot%_datadir/sounds
done


%post
if [ -f %_sysconfdir/X11/window-managers.rpmsave ];then
	%_sbindir/convertsession -f %_sysconfdir/X11/window-managers.rpmsave || :
fi
# Create a link to allow users to access to Mandriva Linux's backgrounds from KDE
[ ! -d %_datadir/wallpapers ] && install -d -m 0755 %_datadir/wallpapers
[ ! -e %_datadir/wallpapers/mandrake-linux ] && ln -s %_datadir/mdk/backgrounds/ %_datadir/wallpapers/mandrake-linux
%update_menus

%make_session
%update_icon_cache hicolor 2> /dev/null

%postun
# Remove link created to allow users to access to Mandriva Linux's backgrounds from KDE
[ -e %_datadir/wallpapers ] && rm -f %_datadir/wallpapers/mandrake-linux
[ $(ls %_datadir/wallpapers/ | wc -l) -eq 0 ] && rm -fr %_datadir/wallpapers/
%clean_menus
%clean_icon_cache hicolor 2> /dev/null

%clean
rm -fr %buildroot



%files
%defattr(-,root,root,-)
%_bindir/*
#
%_sbindir/*

%_sysconfdir/X11/xinit.d/*
%_sysconfdir/profile.d/*
%dir %_sysconfdir/menu.d
%dir %_sysconfdir/xdg
%dir %_sysconfdir/xdg/menus
%dir %_sysconfdir/xdg/menus/applications-merged
%config(noreplace) %_sysconfdir/xdg/menus/*.menu
%dir %_var/lib/menu

#
%dir %_datadir/faces/
%dir %_datadir/mdk/
%dir %_datadir/mdk/faces/
%_datadir/faces/*
%_datadir/mdk/faces/*
#
%dir %_datadir/mdk/backgrounds/
%_datadir/mdk/backgrounds/*.jpg

%dir %_datadir/mdk/bookmarks
%dir %_datadir/mdk/bookmarks/konqueror
%_datadir/mdk/bookmarks/konqueror/*.xml
%dir %_datadir/mdk/bookmarks/mozilla
%_datadir/mdk/bookmarks/mozilla/*.html
#
%dir %_datadir/apps/kdm/pics/
%_datadir/apps/kdm/pics/*
#
%dir %_datadir/mdk/xfdrake/
%_datadir/mdk/xfdrake/*.png
#

%_datadir/sounds/*.wav

%_datadir/mdk/dm

%_datadir/mdk/desktop
#
%_iconsdir/*.png
%_liconsdir/*.png
%_miconsdir/*.png
%_datadir/icons/hicolor/*/*/*.png

%_datadir/desktop-directories/*.directory


