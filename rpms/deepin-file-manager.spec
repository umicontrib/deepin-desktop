%global repo dde-file-manager

Name:           deepin-file-manager
Version:        4.7.7
Release:        2%{?dist}
Summary:        Deepin File Manager
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-file-manager
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  deepin-gettext-tools
BuildRequires:  deepin-dock-devel
BuildRequires:  file-devel
BuildRequires:  jemalloc-devel
BuildRequires:  cmake(KF5Codecs)
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(dframeworkdbus) >= 2.0
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(poppler-cpp)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-qt5-1)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  qt5-linguist

# run command by QProcess
Requires:       deepin-shortcut-viewer
Requires:       deepin-terminal
Requires:       deepin-desktop
Requires:       file-roller
Requires:       gvfs-client
Requires:       samba
Requires:       xdg-user-dirs
Requires:       gstreamer-plugins-good
Recommends:     deepin-manual

%description
File manager front end of Deepin OS.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%package -n deepin-desktop
Summary:        Deepin desktop environment - desktop module
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       deepin-dock
Requires:       deepin-launcher
Requires:       deepin-session-ui

%description -n deepin-desktop
Deepin desktop environment - desktop module.

%prep
%setup -q -n %{repo}-%{version}

# fix file permissions
find -type f -perm 775 -exec chmod 644 {} \;
sed -i '/target.path/s|lib|%{_lib}|' dde-dock-plugins/disk-mount/disk-mount.pro
sed -i '/deepin-daemon/s|lib|libexec|' dde-zone/mainwindow.h
sed -i 's|lib/gvfs|libexec|' %{repo}-lib/gvfs/networkmanager.cpp
sed -i 's|%{_datadir}|%{_libdir}|' dde-sharefiles/appbase.pri

%build
export PATH=%{_qt5_bindir}:$PATH
%qmake_qt5 PREFIX=%{_prefix} QMAKE_CFLAGS_ISYSTEM= CONFIG+="DISABLE_FFMPEG DISABLE_ANYTHING"
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{repo}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/dde-computer.desktop ||:
desktop-file-validate %{buildroot}%{_datadir}/applications/dde-trash.desktop ||:

%ldconfig_scriptlets

%files
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.deepin.filemanager.daemon.conf
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{repo}-xdg-autostart.desktop
%{_bindir}/%{repo}
%{_bindir}/%{repo}-daemon
%{_bindir}/%{repo}-pkexec
%{_bindir}/dde-property-dialog
%{_bindir}/dde-xdg-user-dirs-update
%{_bindir}/usb-device-formatter
%{_bindir}/usb-device-formatter-pkexec
%{_libdir}/lib%{repo}.so.*
%{_libdir}/dde-dock/plugins/
%{_libdir}/%{repo}/
%{_datadir}/%{repo}/
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/applications/%{repo}.desktop
%{_datadir}/dbus-1/interfaces/com.deepin.filemanager.filedialog.xml
%{_datadir}/dbus-1/interfaces/com.deepin.filemanager.filedialogmanager.xml
%{_datadir}/dbus-1/services/com.deepin.filemanager.filedialog.service
%{_datadir}/dbus-1/services/org.freedesktop.FileManager.service
%{_datadir}/dbus-1/system-services/com.deepin.filemanager.daemon.service
%dir %{_datadir}/usb-device-formatter
%{_datadir}/usb-device-formatter/translations/
%{_unitdir}/dde-filemanager-daemon.service
%{_polkit_qt_policydir}/com.deepin.filemanager.daemon.policy
%{_polkit_qt_policydir}/com.deepin.pkexec.dde-file-manager.policy
%{_polkit_qt_policydir}/com.deepin.pkexec.usb-device-formatter.policy

%files devel
%{_includedir}/%{repo}/
%{_includedir}/%{repo}/gvfs/
%{_includedir}/%{repo}/%{repo}-plugins/
%{_includedir}/%{repo}/private/
%{_libdir}/pkgconfig/%{repo}.pc
%{_libdir}/lib%{repo}.so

%files -n deepin-desktop
%{_bindir}/dde-desktop
%{_datadir}/applications/dde-computer.desktop
%{_datadir}/applications/dde-trash.desktop
%dir %{_datadir}/dde-desktop
%{_datadir}/dde-desktop/translations/
%{_datadir}/dbus-1/services/com.deepin.dde.desktop.service

%changelog
* Sun Mar 10 2019 Robin Lee <cheeselee@fedoraproject.org> - 4.7.7-2
- rebuild (Qt5)

* Tue Feb 26 2019 mosquito <sensor.wen@gmail.com> - 4.7.7-1
- Update to 4.7.7

* Tue Feb 19 2019 mosquito <sensor.wen@gmail.com> - 4.7.6-1
- Update to 4.7.6

* Thu Jan 31 2019 mosquito <sensor.wen@gmail.com> - 4.7.5-1
- Update to 4.7.5

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 23 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.10-1
- Update to 4.7.1.10

* Tue Dec 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.7.1.9-2
- rebuild (Qt5)

* Thu Dec 13 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.9-1
- Update to 4.7.1.9

* Thu Dec 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.7.1.4-2
- rebuild (qt5)

* Thu Nov 29 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.4-1
- Update to 4.7.1.4

* Thu Nov 22 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.1-2
- Add Req deepin-session-ui, deepin-dock, deepin-launcher

* Mon Nov 12 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.1-1
- Update to 4.7.1.1

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 4.4.9.1-2
- rebuild (qt5)

* Wed Aug 15 2018 mosquito <sensor.wen@gmail.com> - 4.4.9.1-1
- Update to 4.4.9.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-10
- rebuild (qt5)

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-9
- rebuild (qt5)

* Fri Mar 23 2018 Marek Kasik <mkasik@redhat.com> - 4.4.7-8
- Rebuild for poppler-0.63.0

* Mon Mar 19 2018 mosquito <sensor.wen@gmail.com> - 4.4.7-7
- Exclude ppc64le, ppc64, aarch64

* Sat Mar 10 2018 mosquito <sensor.wen@gmail.com> - 4.4.7-6
- Remove obsoletes statement (BZ#1537223)

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-5
- rebuild (qt5)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.7-3
- Remove obsolete scriptlets

* Mon Jan 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-2
- rebuild (qt5)

* Sat Dec  2 2017 mosquito <sensor.wen@gmail.com> - 4.4.7-1
- Update to 4.4.7

* Mon Nov 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-2
- rebuild (qt5)

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 4.3.4-1
- Update to 4.3.4

* Fri Oct 13 2017 mosquito <sensor.wen@gmail.com> - 4.3.2-1
- Update to 4.3.2
- Remove ffmpeg patch file
- BR: Qt5Concurrent Qt5DBus Qt5Gui

* Wed Oct 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.2.5-2
- BR: qt5-qtbase-private-devel

* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 4.2.5-1
- Update to 4.2.5

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 4.2.4-1
- Update to 4.2.4

* Sun Aug 20 2017 mosquito <sensor.wen@gmail.com> - 4.2.3-1
- Update to 4.2.3

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 4.2.2-1
- Update to 4.2.2

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.1.8-1.git9308953
- Update to 4.1.8

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.1.5-1.git99d7597
- Update to 4.1.5

* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 1.4.1-1.gite303113
- Update to 1.4.1

* Sat Jan 28 2017 mosquito <sensor.wen@gmail.com> - 1.3.8-1.git207000d
- Update to 1.3.8

* Sun Jan 22 2017 mosquito <sensor.wen@gmail.com> - 1.3.7-2.gitf1915f8
- Add Req for run command

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.3.7-1.gitf1915f8
- Update to 1.3.7

* Thu Jan 12 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-3
- Fixed broken icon link noticed by Brenton Horne <brentonhorne77@gmail.com>

* Fri Jan 06 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-2
- Fixed build dependecies

* Fri Dec 30 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-1
- Update package to 1.3.6 and rename to deepin-file-manager

* Mon Dec 19 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.4-1
- Update package to 1.3.4

* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.3-1
- Update package to 1.3.3

* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.3-1
- Initial package build
