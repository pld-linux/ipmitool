Summary:	Simple command-line interface to systems that support the IPMI
Name:		ipmitool
Version:	1.5.9
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmitool/%{name}-%{version}.tar.gz
# Source0-md5:	65ebe0ec6e153d0a1359b907aef5ff13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PMItool is a simple command-line interface to systems that support the
Intelligent Platform Management Interface (IPMI) v1.5 specification.
It provides the ability to read the SDR and print sensor values,
display the contents of the SEL, print FRU information, read and set
LAN configuration parameters, and perform chassis power control.
Originally written to take advantage of IPMI-over-LAN interfaces, it
is also capable of using a system interface as provided by a kernel
device driver such as OpenIPMI.

%prep
%setup -q

%build
%configure \
	--enable-intf-lan \
	--enable-intf-open \
	--enable-ipmievd
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/*
#%{_includedir}/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
