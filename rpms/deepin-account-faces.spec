%global repo dde-account-faces

Name:           deepin-account-faces
Version:        1.0.11
Release:        2%{?dist}
Summary:        Account faces for Linux Deepin
License:        GPLv2+
URL:            https://github.com/linuxdeepin/dde-account-faces
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
BuildArch:      noarch

%description
Account faces for Linux Deepin

%prep
%setup -q -n %{repo}-%{version}

%build

%install
%make_install

%files
%{_sharedstatedir}/AccountsService/icons/*

%changelog
* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov  9 2018 mosquito <sensor.wen@gmail.com> - 1.0.11-1
- Update to 1.0.11

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Sun Oct 09 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.10-1
- Initial package build
