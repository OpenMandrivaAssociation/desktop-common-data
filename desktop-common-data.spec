Summary:	Desktop common files 
Name:		desktop-common-data
Version:	2011.0
Release: 	6
License:	GPL
URL:		http://www.mandriva.com/
Group:		System/Configuration/Other

# get the source from our svn repository (svn+ssh://svn.mandriva.com/svn/soft/desktop-common-data/)
# no extra source or patch are allowed here.
# to generate this tarball, from svn repository above, 
# run "make dist VERSION=%{version} RELEASE=xxmdk"
# where xx is version used for mkrel
Source:		%{name}-%{version}.tar.bz2
Patch0:		desktop-common-data-2011.0-menu.patch
Patch1:         desktop-common-data-2011.0-no-bookmarks.patch

BuildRequires:	intltool
BuildRequires:  menu-messages
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
Requires:	mdk-menu-messages 
Requires:	xdg-utils
Requires:	xdg-user-dirs
Requires:	run-parts
Requires(post):	hicolor-icon-theme
Requires:	hicolor-icon-theme
Conflicts:      kdelibs-common < 30000000:3.5.2

%description
This package contains useful icons, menu structure and others goodies for the
Mandriva Linux desktop.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make

%install
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

#install sound theme Ia Ora
install -d -m 0755 %buildroot%_datadir/sounds/ia_ora/stereo
install -m 0644 sounds/index.theme %buildroot%_datadir/sounds/ia_ora
ln -s ../../ia_ora-startup.wav %buildroot%_datadir/sounds/ia_ora/stereo/desktop-login.wav
ln -s ../../ia_ora-shutdown.wav %buildroot%_datadir/sounds/ia_ora/stereo/desktop-logout.wav
ln -s ../../ia_ora-error.wav %buildroot%_datadir/sounds/ia_ora/stereo/dialog-error.wav
ln -s ../../ia_ora-notification.wav %buildroot%_datadir/sounds/ia_ora/stereo/dialog-warning.wav
touch  %buildroot%_datadir/sounds/ia_ora/stereo/dialog.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/power.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/battery.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/suspend.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/screen-capture.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/service.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/system.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/desktop.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/device.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/bell.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/message-new-email.disabled
touch  %buildroot%_datadir/sounds/ia_ora/stereo/trash-empty.disabled


%post
if [ -f %_sysconfdir/X11/window-managers.rpmsave ];then
	%_sbindir/convertsession -f %_sysconfdir/X11/window-managers.rpmsave || :
fi
%make_session
# (cg) See sound-theme-freedesktop for explanation about touch.
touch --no-create %_datadir/sounds %_datadir/sounds/ia_ora

%postun
# (cg) See sound-theme-freedesktop for explanation about touch.
touch --no-create %_datadir/sounds %_datadir/sounds/ia_ora

%triggerin -- %{_datadir}/applications/*.desktop, %{_datadir}/applications/*/*.desktop
%{_bindir}/update-menus

%triggerin -- %{_datadir}/X11/dm.d/*.conf, %{_sysconfdir}/X11/wmsession.d/*
%{_sbindir}/fndSession

%triggerpostun -- %{_datadir}/applications/*.desktop, %{_datadir}/applications/*/*.desktop
%{_bindir}/update-menus

%triggerpostun -- %{_datadir}/X11/dm.d/*.conf, %{_sysconfdir}/X11/wmsession.d/*
%{_sbindir}/fndSession

%clean
rm -fr %buildroot

%files
%defattr(-,root,root,-)
%_bindir/*
#
%_sbindir/*

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
%_datadir/sounds/ia_ora

%_datadir/mdk/dm

%dir %_datadir/mdk/desktop
%dir %_datadir/mdk/desktop/free
%dir %_datadir/mdk/desktop/one
%dir %_datadir/mdk/desktop/powerpack
%attr(0755,root,root) %_datadir/mdk/desktop/*/*
#
%_iconsdir/*.png
%_liconsdir/*.png
%_miconsdir/*.png
%_datadir/icons/hicolor/*/*/*.png

%_datadir/desktop-directories/*.directory




%changelog
* Wed Aug 17 2011 Andrey Bondrov <abondrov@mandriva.org> 2011.0-5mdv2011.0
+ Revision: 695030
- Add patch0 to make better XDG menu layout (fix some submenu positions)

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2011.0-4
+ Revision: 663764
- mass rebuild

* Fri Apr 01 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 2011.0-3
+ Revision: 649623
- Remove support for old distributions
  Add new Faces

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 2011.0-2
+ Revision: 640266
- rebuild to obsolete old packages

* Tue Feb 15 2011 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 2011.0-1
+ Revision: 637855
- New version: 2011.0

* Sun Feb 13 2011 Funda Wang <fwang@mandriva.org> 2010.1-6
+ Revision: 637615
- split triggers

* Sun Feb 13 2011 Funda Wang <fwang@mandriva.org> 2010.1-4
+ Revision: 637539
- revert to 2010.1
- rename tarball
- convert trigger into rpm5 file trigger

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2010.1-3mdv2011.0
+ Revision: 604784
- rebuild

* Wed Jun 16 2010 Frederic Crozat <fcrozat@mandriva.com> 2010.1-2mdv2010.1
+ Revision: 548169
- Fix chksession 'default' return (pzanoni, Mdv bug #59733)
- Fix Security tagged items not being displayed (Mdv bug #59087)
- Ensure submenus are not inlined in Tools menu

* Thu Mar 18 2010 Frederic Crozat <fcrozat@mandriva.com> 2010.1-1mdv2010.1
+ Revision: 525011
- Release 2010.1 :
 - fix non top-level menus to use inlining by default (one level)
 - fix xvt to be KDE4 compliant and start konsole in no-fork mode (pzanoni, Mdv bug #57052)

* Fri Nov 06 2009 Frederic Crozat <fcrozat@mandriva.com> 2010.0-5mdv2010.1
+ Revision: 461449
- Ensure Openoffice is at the top of Office menu and remove ooo64 entries

* Tue Oct 27 2009 Frederic Crozat <fcrozat@mandriva.com> 2010.0-4mdv2010.0
+ Revision: 459566
- Disable more sounds in ia_ora sound theme

* Tue Oct 27 2009 Frederic Crozat <fcrozat@mandriva.com> 2010.0-3mdv2010.0
+ Revision: 459520
- Upgrade .desktop launcher to use new urls

* Wed Sep 30 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2010.0-2mdv2010.0
+ Revision: 451894
- Fix perms of desktop files

* Wed Aug 19 2009 Frederic Crozat <fcrozat@mandriva.com> 2010.0-1mdv2010.0
+ Revision: 417953
- Release 2010.0 :
 - fix bashism in menustyle.sh
 - rename mandrake.png icon to mandriva.png

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2009.1-3mdv2010.0
+ Revision: 413347
- rebuild

* Wed Mar 18 2009 Frederic Crozat <fcrozat@mandriva.com> 2009.1-2mdv2009.1
+ Revision: 357399
- Add support for pam-message in gdm theme (Mdv bug #45081)
- Fix jamendo url in bookmarks
- Icon support for fluxbox menu (Mdv bug #48522, patch From Jorge Van Hemelryck)
- Fix default bookmarks (spuk, Mdv bug #47097)

* Tue Mar 03 2009 Frederic Crozat <fcrozat@mandriva.com> 2009.1-1mdv2009.1
+ Revision: 347987
- Release 2009.1 :
 - update some bookmarks (spuk)
 - add support for lxterminal in xvt

* Fri Oct 03 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-12mdv2009.0
+ Revision: 291051
- Fix screenshots for gdm / kdm (Mdv bug #44568)

* Mon Sep 29 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-11mdv2009.0
+ Revision: 289171
- Update menu file to put KDE4 control center at the beginning of menu list

* Tue Sep 16 2008 Colin Guthrie <cguthrie@mandriva.org> 2009.0-10mdv2009.0
+ Revision: 285182
- Touch /usr/share/sounds to invalidate libcanberra cache

* Thu Sep 11 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-9mdv2009.0
+ Revision: 283836
- Tune gdm theme for better readability with pwp/one backgrounds
- Move DiscBurning to Tools (Mdv bug #42598)

* Tue Aug 19 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-8mdv2009.0
+ Revision: 273889
- Disable more sound events by default
- Don't create empty postun script on 2009.0

* Tue Aug 12 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-7mdv2009.0
+ Revision: 271104
- Add sound theme
- remove old migration scripts
- Fix www-browser to detect KDE4 (Luc Menut, Mdv bug #42558)

* Mon Aug 04 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-6mdv2009.0
+ Revision: 263307
- Update gdm theme to use .jpg file, gtk doesn't load .jpg file named .png anymore

* Tue Jul 08 2008 Pixel <pixel@mandriva.com> 2009.0-5mdv2009.0
+ Revision: 232644
- add rpm filetrigger running fndSession when rpm install/remove dm.d or wmsession.d files

* Mon Jun 30 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-4mdv2009.0
+ Revision: 230263
- Fix fndSession to use new dm.d path (Mdv bug #41712)
- Add terminal to possible terminal emulator list in xvt

* Tue Jun 24 2008 Frederic Crozat <fcrozat@mandriva.com> 2009.0-3mdv2009.0
+ Revision: 228718
- Update xdm Xsession path in chksession (Mdv bug #41645)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - normalize call to %%update_icon_cache/%%clean_icon_cache

* Thu Jun 05 2008 Pixel <pixel@mandriva.com> 2009.0-2mdv2009.0
+ Revision: 215699
- add rpm filetrigger running update-menus when rpm install/remove .desktop files

* Mon May 05 2008 Helio Chissini de Castro <helio@mandriva.com> 2009.0-1mdv2009.0
+ Revision: 201560
- Enable chksession to understand new paths from kde3 and been able to generate sessions for kdm 3 and 4

* Mon Mar 31 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-8mdv2008.1
+ Revision: 191255
- Rebuild with latest translations
- Add requires on run-parts (Mdv bug #39519)

* Mon Mar 17 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-7mdv2008.1
+ Revision: 188256
- Rebuild to get latest translations

* Fri Mar 14 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-6mdv2008.1
+ Revision: 187939
- Update text for register icon
- New bookmarks for 2008.1

* Mon Mar 10 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-5mdv2008.1
+ Revision: 183692
- Update screenshots for gdm and kdm
- Increase size for faces (Mdv bug #38604)

* Wed Mar 05 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-4mdv2008.1
+ Revision: 180167
- Add files needed for GDM Mandriva theme (version without user list)

* Wed Mar 05 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-3mdv2008.1
+ Revision: 180007
- fix small size of user list for gdm greeter
- fix icewm / twm detection in chkconfig (blino)

* Fri Feb 29 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-2mdv2008.1
+ Revision: 176770
- Update kdm theme to use Bold text for welcome screen

* Thu Feb 28 2008 Frederic Crozat <fcrozat@mandriva.com> 2008.1-1mdv2008.1
+ Revision: 176401
- New gdm/kdm theme
- new faces
- drop dependency on mandriva-theme, packages which need a background should requires mandriva-theme directly

* Thu Feb 07 2008 Danilo Cesar Lemes de Paula <danilo@mandriva.com> 2008.0-20mdv2008.1
+ Revision: 163652
+ rebuild (emptylog)

* Mon Jan 07 2008 Danilo Cesar Lemes de Paula <danilo@mandriva.com> 2008.0-19mdv2008.1
+ Revision: 146289
- dm/KdmGreeterTheme.desktop was edited to use a KDM screenshot file (screenshot_kdm.png) instead a GDM's screenshot file

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Dec 22 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2008.0-18mdv2008.1
+ Revision: 137215
- no executable bit on profile scriptlets
  order prefix on profile scriptlets

* Wed Dec 19 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-17mdv2008.1
+ Revision: 134752
- update Ia Ora sound samples with 22kHz 16bits version (helio)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 23 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-16mdv2008.1
+ Revision: 101528
- Fix query for Tools menu (Mdv bug #34957)
- Make sure package can be backported to 2008.0

  + Funda Wang <fwang@mandriva.org>
    - mdk-menu-messages has been renamed to menu-messages

* Wed Oct 03 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-15mdv2008.0
+ Revision: 94939
- Regenerate tarball, 14mdv didn't have the change advertised in the changelog

* Mon Oct 01 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-14mdv2008.0
+ Revision: 94126
- Fix menu to no longer hide System;Settings;GNOME in SystemTools (Mdv bug #34269)
- Update url for register launcher
-

* Fri Sep 28 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-13mdv2008.0
+ Revision: 93690
- Fix desktop launcher again (Mdv bug #34235, 34238)

* Thu Sep 27 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-12mdv2008.0
+ Revision: 93312
- Tune menus to put .desktop with only main categories (usually from ISV) at top level. Bring 100%% compliance with XDG utils test suite
- Add support for OOo 64bits .desktop
- Fix typo in ParallelComputing category
- Printing and PackageManager are no longer desktop dependant (Mdv bug #33766, #33436)
- hide Emulator / HardwareSettings from Tools/More (Mdv bug #33765, #33906)
- Add new icon for Register launcher

* Wed Sep 19 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-11mdv2008.0
+ Revision: 90963
- Group kcontrol with MCC in System tools (Mdv bug #33663)
- Hide rpmdrake in SystemTools
- update translations for dekstop launchers
- Add icons for desktop launcher in hicolor icon theme
- Fix textcolor in mouseover for gdm/kdm theme

* Mon Sep 17 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-10mdv2008.0
+ Revision: 89294
- Fix gdm / kdm theme to show menu icon correctly
- Fix menu to move OO.o Draw to correct layout section (Mdv bug #33651)

* Fri Sep 14 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-9mdv2008.0
+ Revision: 85665
- Remove special case for drakconf in menu (fixed in its .desktop)
- Import new 2008 dm theme and port it to gdm
- Import Ia Ora Sound theme, authored by Helio (congrat)
- add new default launchers for desktop

* Mon Sep 10 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-8mdv2008.0
+ Revision: 84220
- Make sure all GNOME System but not Settings apps are visible in SystemTools
- update xdg_menu with gnomesu path (SUSE)

  + Adam Williamson <awilliamson@mandriva.org>
    - s/Mandrakelinux/Mandrivalinux/

* Fri Sep 07 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-7mdv2008.0
+ Revision: 81947
- Improve KDM theme
- Add support for X-MandrivaLinux-More category
- Enable inlining on More submenus
- re-add Preferences/Advanced .directory for GNOME panel

* Thu Aug 30 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-6mdv2008.0
+ Revision: 75765
- Update bookmarks for 2008.0
- Really fix missing icons for graphics/more (Mdv bug #32839)
- Exclude Emulators from SystemTools menu (Mdv bug #32940)
- Use new rpmdrake .desktop filename

* Tue Aug 28 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-5mdv2008.0
+ Revision: 72760
- don't show Emulators in Tools/More (Austin)
- fix xdg_menu to not call kde-config as root (Mdv bug #32847)

* Mon Aug 27 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-4mdv2008.0
+ Revision: 71914
- Put xdg_menu cache in /var/lib/menu (pixel)

* Mon Aug 27 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-3mdv2008.0
+ Revision: 71810
-Add missing .directory for graphics/more (Mdv bug #32839)
-Rebuild with additional translations (Mdv bug #32884)

* Fri Aug 24 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-2mdv2008.0
+ Revision: 71033
- New Mandriva menu (based on Frederik Himpe proposal)

* Mon Aug 06 2007 Frederic Crozat <fcrozat@mandriva.com> 2008.0-1mdv2008.0
+ Revision: 59440
- New release for 2008.0 :
 - mdk-folders are dead, we are now using XDG user directories instead
- Check if %%_install_langs is set to all before allowing build

* Fri May 11 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-12mdv2008.0
+ Revision: 26375
- add support for gdm 2.19.x new background property
- fix handling of zh locale for desktop directories (Mdv bug #30216)
- Fix www-browser call (Mdv bug #30522) (mrl)


* Wed Apr 04 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-11mdv2007.1
+ Revision: 150572
- Fix KDELegacy node position, causing empty Other menu node (Mdv bug #30126)

* Tue Apr 03 2007 Olivier Blin <oblin@mandriva.com> 2007.1-10mdv2007.1
+ Revision: 150302
- use fbrun in fluxbox menu instead of bbrun (#30076)
- do not hardcode xterm menu entry for fluxbox (#30076)

* Sat Mar 31 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-9mdv2007.1
+ Revision: 150100
- Update menu for discovery : hide more entries, make sure all accessibility tools are in "More applications"
- Update main menu : accept old categories which are still in specification

* Sat Mar 31 2007 Laurent Montel <lmontel@mandriva.com> 2007.1-8mdv2007.1
+ Revision: 150007
- Fix duplicate entries

* Wed Mar 28 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-7mdv2007.1
+ Revision: 149183
- Fix title for some konqueror bookmarks
- Don't output errors in fndSession when no session file is present

* Thu Mar 22 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-6mdv2007.1
+ Revision: 148136
- Fix Discovery menu

* Thu Mar 22 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-5mdv2007.1
+ Revision: 148058
- Update menu entries for One / Discovery

* Wed Mar 21 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-4mdv2007.1
+ Revision: 147486
- Prevent building when menu-message is broken
- update bookmarks
- fix www-browser loop

* Thu Mar 15 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-3mdv2007.1
+ Revision: 144412
- Add .desktop files for nautilus default desktop for One / Free
- Fix garbaged png/jpg files (Mdv bug #29005)
- (mrl) www-browser works for KDE and uses xdg-open when relevant (Mdv bug #16920)
- Hide GNOME Configuration subtree in main menu (Mdv bug #29270)
- Fix some url / names for konqueror bookmarks (Mdv bug #27964)

* Thu Feb 22 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-2mdv2007.1
+ Revision: 124422
- Update star icon

* Fri Feb 16 2007 Frederic Crozat <fcrozat@mandriva.com> 2007.1-1mdv2007.1
+ Revision: 122000
- Remove xinitrc dependency (Mdv bug #26739)
- Fix fndSession umask (Mdv bug #17707)
- Add freedesktop.org categories to menu files (Mdv bug #26709)

* Wed Feb 14 2007 Laurent Montel <lmontel@mandriva.com> 2007-21mdv2007.1
+ Revision: 121159
- Fix bookmarks
- Import desktop-common-data

* Thu Nov 16 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-20mdv2007.0
- Fix incorrect category for wordprocessors in discovery menu (Mdv bug #27084)

* Fri Oct 27 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-19mdv2007.0
- Fix update-menus script to not output empty line
- Re-add menu file stamp to prevent restarting update-menus for each
  graphical login

* Tue Oct 03 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-18mdv2007.0
- Rename root node from Mandriva Linux to Applications (Mdv bug #25389)
- Add missing .directory for various entries (Mdv bug #26273)

* Tue Sep 26 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-17mdv2007.0
- Add missing Emulator category to menu files (Mdv bug #26148)

* Fri Sep 22 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-16mdv2007.0
- Hide more applications in one products
- Increase version for Conflicts (Mdv bug #26043)

* Wed Sep 20 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-15mdv2007.0
- Fix error in upstream category in main menu
- add mandriva-discovery.menu additional menu file to hide / sort applications
  for Discovery / One products

* Tue Sep 19 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-14mdv2007.0
- Rebuild with fixed mdk-menu-message to get all translations (Mdv bug #25895)

* Thu Sep 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-13mdv2007.0
- Update with new bookmarks
- Don't show GNOME configuration in standard menu, moved in preferences menu

* Sat Sep 09 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-12mdv2007.0
- Update profile scripts to remove invalid dependencies
- move defaults bookmarks from kde and firefox to this package

* Tue Sep 05 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-11mdv2007.0
- Improve gdm/kdm theme with new backgrounds
- Don't create default desktop directories for root (Mdv bug #19711)

* Fri Sep 01 2006 Laurent MONTEL <lmontel@mandriva.com> 2007-10mdv2007.0
- Fix upgrade from 2006
- Fix discovery menu (merge kmenuedit.menu when it created by kmenuedit, fix 
 kfmclient error)

* Thu Aug 31 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-9mdv2007.0
- update-menus doesn't do anything if DURING_INSTALL is set to 1

* Thu Aug 31 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-8mdv2007.0
- Add missing directory file for adventure (Mdv bug #24829)
- Add empty menu nodes for KDE in discovery menu
- Remove old X-MandrakeLinux* categories for main menu, all entries
  must now use X-MandrivaLinux
- fix default directories creation if translation contains spaces (Mdv bug #24677)

* Fri Aug 18 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-7mdv2007.0
- Add discovery menu and script to support MDV_MENU_STYLE

* Fri Aug 18 2006 Laurent MONTEL <lmontel@mandriva.com> 2007-6
- Change requires to mandriva-theme

* Thu Aug 10 2006 Laurent MONTEL <lmontel@mandriva.com> 2007-5
- Fix oowriter menu entry

* Tue Aug 08 2006 Laurent MONTEL <lmontel@mandriva.com> 2007-4
- Fix applications-mdk.menu to merge kmenuedit.menu files (fix mdk bug #24103)

* Fri Jul 21 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-3mdv2007.0
- Ignore "Development" keyword, it is too broad atm (Mdv bug #23826)
- Add .directory for Archiving/Other (Mdv bug #23845)

* Fri Jul 21 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-2mdv2007.0
- Fix some typo (Andrej) (Mdk bug #23842)

* Tue Jul 18 2006 Frederic Crozat <fcrozat@mandriva.com> 2007-1mdv2007.0
- Drop old menu system completely

* Wed Jul 12 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-12mdv2007.0
- Add missing .directory (Mdv bug #23614)
- fix translations for some .directories (Mdv bug #23641)

* Sat Jul 08 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-11mdv2007.0
- add missing .directory
- rebuild with fixed intltool
- fix generating icewm menu from XDG (pixel)

* Tue Jun 20 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-10mdv2007.0
- Add missing .directory files and fix videoconference one

* Fri Jun 16 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-9mdv2007.0
- Switch to X-MandrivaLinux

* Tue May 30 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-8mdv2007.0
- Add legacy directories and default merge directory

* Thu May 18 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-7mdk
- ship our own .directory files now
- use kde .directory files when possible
- add more upstream categories

* Sat May 13 2006 Laurent MONTEL <lmontel@mandriva.com> 2006-6
- Update for missing kcontrol entry

* Fri May 12 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-5mdk
- Update menu file with new filename for kde

* Thu May 11 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-4mdk
- Add missing catergories in menu file (laurent)

* Fri May 05 2006 Frederic Crozat <fcrozat@mandriva.com> 2006-3mdk
- Add applications-mdk.menu file for XDG menu system
- Add xdg_menu script from SUSE to support old WM
- Don't ship defaultlayout.menu anymore, it is merged into main menu
- Fix typo in old menu file

* Tue Sep 27 2005 Frederic Crozat <fcrozat@mandriva.com> 2006-2mdk 
- Fix desktop-directory script (UTF encoded URL, hidden .directory file)
  Mdk bug #18853

* Sat Sep 24 2005 Frederic Lepied <flepied@mandriva.com> 2006-1mdk
- Mandriva
- fixed simplified menu

* Tue Sep 20 2005 Laurent MONTEL <lmontel@mandriva.com> 10.3.1-9mdk
- Fix menu order

* Tue Sep 20 2005 Frederic Crozat <fcrozat@mandriva.com> 10.3.1-8mdk 
- Fix loop in www-browser (based on patch from Andrey Borzenkov)

* Tue Sep 13 2005 Frederic Crozat <fcrozat@mandriva.com> 10.3.1-7mdk 
- Fix package name and command for gimp in simplified menu (Mdk bug #17627)

* Fri Sep 09 2005 Laurent MONTEL <lmontel@mandriva.com> 10.3.1-6mdk
- Add separator in simplified menu

* Tue Aug 30 2005 Frederic Crozat <fcrozat@mandriva.com> 10.3.1-5mdk 
- Fix default directories script when no translation is available

* Sat Aug 27 2005 Frederic Crozat <fcrozat@mandriva.com> 10.3.1-4mdk 
- New scheme for default directories

* Thu Aug 25 2005 Frederic Crozat <fcrozat@mandriva.com> 10.3.1-3mdk 
- Add default directories xinit.d script

* Wed Aug 24 2005 Laurent MONTEL <lmontel@mandriva.com> 10.3.1-2mdk
- Mandrake->Mandriva

* Tue Jun 07 2005 Frederic Lepied <flepied@mandriva.com> 10.3.1-1mdk
- rebuild to have the correct fndSession (bug #16255)

* Tue May 31 2005 Frederic Lepied <flepied@mandriva.com> 10.3-1mdk
- fndSession: use the new generic framework

* Sat May 14 2005 Frederic Crozat <fcrozat@mandriva.com> 10.2-5mdk 
- change package name
- xvt : fix typo (bug #15836)
- fix typo in translation-map
- remove screensaver images, moved in theme package

* Wed Mar 30 2005 Frederic Lepied <flepied@mandrakesoft.com> 10.2-4mdk
- www-browser: test if the $BROWSER variable is set to something valid (bug #14903).

* Wed Mar 23 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 10.2-3mdk 
- don't use .desktop files for order directive

* Wed Mar 09 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 10.2-2mdk 
- change www-browser to use BROWSER variable if set or use running environment
  settings if set.
- xvt script to replace alternative : choose programs to start based on
  running environment

* Mon Mar 07 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 10.2-1mdk
- Fix error into menu

* Wed Mar 02 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 10.1-19mdk
- Fix order for simplified menu

* Tue Mar 01 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 10.1-18mdk
- Fix Filename order with menu id

* Tue Mar 01 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 10.1-17mdk
- Update menu order

* Mon Feb 28 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 10.1-16mdk 
- Install shared Mdk theme for GDM/KDM

* Tue Jan 25 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 10.1-15mdk 
- Fix small errors in default layout menu files

* Tue Dec 14 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 10.1-14mdk 
- Move mdk menu data from menu to mandrake_desk package

* Thu Sep 30 2004 David Baudens <baudens@mandrakesoft.com> 10.1-13mdk
- Fix task oriented menu to allow translations of "Listen to Music Files" menu
  entry (Laurent Montel)

* Thu Sep 30 2004 David Baudens <baudens@mandrakesoft.com> 10.1-12mdk
- Add missing menu entry for french Mandrakelinux documentation

* Thu Sep 30 2004 David Baudens <baudens@mandrakesoft.com> 10.1-11mdk
- Fix Import and Sort Your Photos menu entry

* Sat Sep 11 2004 David Baudens <baudens@mandrakesoft.com> 10.1-10mdk
- Add documentation to task oriented menu

* Fri Sep 10 2004 David Baudens <baudens@mandrakesoft.com> 10.1-9mdk
- Remove all longtitle

* Fri Sep 10 2004 David Baudens <baudens@mandrakesoft.com> 10.1-8mdk
- Fix task oriented menu (kphone)

* Thu Sep 02 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 10.1-7mdk
- Fix capitalization in simplified menu

* Wed Sep 01 2004 Frederic Lepied <flepied@mandrakesoft.com> 10.1-6mdk
- added the script www-browser

* Sat Aug 28 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 10.1-5mdk
- Fix typo in gnome-cd entry

* Tue Aug 17 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 10.1-4mdk
- Fix "Play Games" menu entry

* Thu Aug 12 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 10.1-3mdk
- Add GNOME version of task oriented menu
- Fix capitalisations in task oriented menu

* Fri Aug 06 2004 David Baudens <baudens@mandrakesoft.com> 10.1-2mdk
- Add "Make a phone call" to task oriented menu

* Fri Aug 06 2004 David Baudens <baudens@mandrakesoft.com> 10.1-1mdk
- Update task oriented menu

* Thu Aug 05 2004 Pixel <pixel@mandrakesoft.com> 10.0-11mdk
- add "chksession -L" used by DrakX to configure ~/.dmrc
- fix descriptions (use Mandrakelinux instead of simply Mandrake)

