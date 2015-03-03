%define __jar_repack 0

Name: opendaylight
Summary: OpenDaylight SDN Controller
Version: helium
Release: 3
Source0: https://nexus.opendaylight.org/content/groups/public/org/opendaylight/integration/distribution-karaf/0.2.2-Helium-SR2/distribution-karaf-0.2.2-Helium-SR2.tar.gz
Source1: opendaylight-service.tar.gz
Patch0: opendaylight-helium-remove_credentials.patch
Group: Applications/Communications
License: EPL-1.0
URL: http://www.opendaylight.org
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot

Requires: java-1.7.0-openjdk-devel >= 1.7.0
Requires(pre): shadow-utils
BuildRequires: systemd

%pre
# Create odl user/group
getent passwd odl > /dev/null || useradd odl -M -d $RPM_BUILD_ROOT/opt/%name/%name-%version
getent group odl > /dev/null || groupadd odl

# disable debug packages and the stripping of the binaries
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
OpenDaylight is an open platform for network programmability to enable SDN and create a solid foundation for NFV for networks at any size and scale.

%prep
%setup -q -b 1 -n opendaylight-service
%setup -q -b 0 -n distribution-karaf-0.2.2-Helium-SR2
%patch0 -p0

%build

%install
mkdir -p $RPM_BUILD_ROOT/opt/%{name}/%{name}-%{version}
cp -r ../distribution-karaf-0.2.2-Helium-SR2/* $RPM_BUILD_ROOT/opt/%{name}/%{name}-%{version}
# Create dir in build root for systemd .service file and copy it over
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp ../opendaylight-service/opendaylight.service $RPM_BUILD_ROOT/%{_unitdir}

%clean
rm -rf $RPM_BUILD_ROOT
 
%post
echo " "
echo "OpenDaylight Helium successfully installed"

%postun
rm -rf $RPM_BUILD_ROOT/opt/%{name}/%{name}-%{version}

%files
# ODL uses systemd to run as user:group odl:odl
%attr(0775,odl,odl) /opt/%name/%name-%version/
%attr(0644,-,-) %{_unitdir}/%name.service

%changelog
* Mon Feb 23 2015 David Jorm - helium-3
- Added systemd integration, removed default karaf credentials
* Sun Feb 01 2015 David Jorm - helium-2
- Upgraded to helium SR2
* Tue Jan 20 2015 David Jorm - helium-1
- Added openjdk-devel dependency
* Fri Jan 16 2015 David Jorm - helium-0
- Initial creation
