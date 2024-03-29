%define __jar_repack 0

Name: opendaylight-helium
Summary: OpenDaylight SDN Controller
Version: 3
Release: 2%{?dist}
Source0: https://nexus.opendaylight.org/content/groups/public/org/opendaylight/integration/distribution-karaf/0.2.4-Helium-SR4/distribution-karaf-0.2.4-Helium-SR4.tar.gz
Source1: opendaylight-helium.service
Patch0: 0001-opendaylight-helium-remove-credentials.patch
Group: Applications/Communications
License: EPL-1.0
URL: http://www.opendaylight.org
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot

Requires: java-1.7.0-openjdk-devel >= 1.7.0
Requires(pre): shadow-utils, glibc-common
Requires(postun): shadow-utils
BuildRequires: systemd

# this is used to identify if we need to remove the odl user/group when
# removing
Provides: opendaylight

%pre
%global odl_user odl
%global odl_home /opt/opendaylight

# Create odl user/group
getent passwd %{odl_user} > /dev/null \
    || useradd --system --home-dir %{odl_home} %{odl_user}
getent group %{odl_user} > /dev/null \
    || groupadd --system %{odl_user}

# disable debug packages and the stripping of the binaries
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
OpenDaylight is an open platform for network programmability to enable SDN and create a solid foundation for NFV for networks at any size and scale.

%prep
ROOT_DIR=$(dirname $(tar -tf %{SOURCE0} | head -n 1))
%autosetup -N -c -n %{name}
mv ${ROOT_DIR}/* .
rm -rf ${ROOT_DIR}
%autopatch -p0

%build

%install
install -d %{buildroot}/%{odl_home}
cp -R %{_builddir}/%{name} %{buildroot}/%{odl_home}
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service

%clean
rm -rf %
 
%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

# remove installed files
rm -rf %{odl_home}/%{name}

# remove odl user/group if no other opendaylight package is installed
rpmquery --query --whatprovides opendaylight > /dev/null \
    || { userdel %{odl_user} && groupdel %{odl_user}; }

%files
# ODL uses systemd to run as user:group odl:odl
%attr(0775,odl,odl) %{odl_home}/%{name}
%attr(0644,-,-) %{_unitdir}/%{name}.service

%changelog
* Tue Dec 29 2015 John Siegrist <john@complects.com> - 3-2
- Upgraded to helium SR4.
* Fri Mar 20 2015 David Jorm - 3-1
- Upgraded to helium SR3
* Wed Mar 04 2015 Arun Babu Neelicattu <abn@iix.net> - 2-4
- Rename package to opendaylight-helium-version-release, use macros instead of
  variables, update spec file to use autosetup, add opendaylight virtual
  capability, rename service to reflect new package name.
* Mon Feb 23 2015 David Jorm - helium-3
- Added systemd integration, removed default karaf credentials
* Sun Feb 01 2015 David Jorm - helium-2
- Upgraded to helium SR2
* Tue Jan 20 2015 David Jorm - helium-1
- Added openjdk-devel dependency
* Fri Jan 16 2015 David Jorm - helium-0
- Initial creation
