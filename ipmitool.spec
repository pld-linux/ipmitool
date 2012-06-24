Summary:	Simple command-line interface to systems that support the IPMI
Summary(pl):	Prosty dzia�aj�cy z linii polece� interfejs do system�w obs�uguj�cych IPMI
Name:		ipmitool
Version:	1.5.9
Release:	2
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmitool/%{name}-%{version}.tar.gz
# Source0-md5:	65ebe0ec6e153d0a1359b907aef5ff13
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IPMItool is a simple command-line interface to systems that support
the Intelligent Platform Management Interface (IPMI) v1.5
specification. It provides the ability to read the SDR and print
sensor values, display the contents of the SEL, print FRU information,
read and set LAN configuration parameters, and perform chassis power
control. Originally written to take advantage of IPMI-over-LAN
interfaces, it is also capable of using a system interface as provided
by a kernel device driver such as OpenIPMI.

%description -l pl
IPMItool to prosty, dzia�aj�cy z linii polece� interfejs do system�w
obs�uguj�cych specyfikacj� Intelligent Platform Management Interface
(IPMI) v1.5. Daje mo�liwo�� odczytu SDR i wypisania warto�ci
czujnik�w, wy�wietlenia zawarto�ci SEL, wypisania informacji FRU,
odczytu i ustawiania parametr�w konfiguracji LAN i sterowania
zasilaniem. Narz�dzie napisano pierwotnie w celu wykorzystania
interfejs�w IPMI-over-LAN, ale mo�liwe jest tak�e u�ywanie interfejsu
systemowego dostarczonego przez sterownik urz�dzenia w j�drze, taki
jak OpenIPMI.

%package devel
Summary:	Header files to write ipmitool plugins
Summary(pl):	Pliki nag��wkowe do tworzenia wtyczek ipmitoola
Group:		Development/Libraries
# doesn't require base

%description devel
Header files to write ipmitool plugins.

%description devel -l pl
Pliki nag��wkowe do tworzenia wtyczek ipmitoola.

%prep
%setup -q

%build
%{__libtoolize} --ltdl
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--enable-intf-lan \
	--enable-intf-open \
	--enable-ipmievd \
	--with-plugin-path=%{_libdir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
# lt_dlopen is used without extension
%{_libdir}/%{name}/*.la
%{_mandir}/man?/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
