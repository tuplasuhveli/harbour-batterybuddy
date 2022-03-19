Name:       harbour-batterybuddy

# >> macros
# << macros

%{!?qtc_qmake:%define qtc_qmake %qmake}
%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}
%{?qtc_builddir:%define _builddir %qtc_builddir}

# Change the version and release strings in .pro file only!

Summary:    Battery Buddy
Version:    3.16.2
Release:    1
Group:      Qt/Qt
License:    GPLv3
URL:        http://example.org/
Source0:    %{name}-%{version}.tar.bz2
Requires:   sailfishsilica-qt5 >= 0.10.9
Requires:   nemo-qml-plugin-configuration-qt5
Requires:   nemo-qml-plugin-notifications-qt5
Requires:   libkeepalive
BuildRequires:  pkgconfig(sailfishapp) >= 1.0.2
BuildRequires:  pkgconfig(nemonotifications-qt5)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  desktop-file-utils
BuildRequires:  libkeepalive-devel

%description
Prolong your battery life.


%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
# << build pre

%qtc_qmake5 

%qtc_make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%qmake5_install

# >> install post
# << install post

desktop-file-install --delete-original       \
  --dir %{buildroot}%{_datadir}/applications             \
   %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root,-)
%{_bindir}/*
%defattr(0644,root,root,-)
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
# >> files
# << files

%posttrans
# Remove old service
systemctl stop %{name}.service
systemctl disable %{name}.service
rm %{_unitdir}/%{name}.service

# Install/update permission daemon (root)
cp %{_datadir}/%{name}/service/%{name}-oneshot.service %{_unitdir}/%{name}-oneshot.service
systemctl daemon-reload
systemctl enable %{name}-oneshot.service
systemctl start %{name}-oneshot.service

# Install/update background daemon (default user)
cp %{_datadir}/%{name}/service/%{name}.service %{_userunitdir}/%{name}.service
systemctl-user daemon-reload
systemctl-user enable %{name}.service
systemctl-user stop %{name}.service
systemctl-user start %{name}.service
exit 0

%postun
// Run on uninstall, not on upgrade
if [ $1 -eq 0 ]; then
  systemctl-user stop %{name}.service"
  systemctl-user disable %{name}.service"
  rm %{_userunitdir}/%{name}.service
  systemctl-user daemon-reload"

  systemctl stop %{name}-oneshot.service
  systemctl disable %{name}-oneshot.service
  rm %{_unitdir}/%{name}-oneshot.service
  systemctl daemon-reload
fi
exit 0
