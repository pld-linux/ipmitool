Summary:	Simple command-line interface to systems that support the IPMI
Summary(pl):	Prosty dzia�aj�cy z linii polece� interfejs do system�w obs�uguj�cych IPMI
Name:		ipmitool
Version:	1.6.0
Release:	1.1
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmitool/%{name}-%{version}.tar.bz2
# Source0-md5:	5f95cfc69531ee783eac5ec3939115b8
Patch0:		%{name}-nodoc.patch
URL:		http://ipmitool.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool
Obsoletes:	ipmitool-devel
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

%prep
%setup -q
# maybe it's just easier to rm -rf installed docs
%patch0 -p1

%build
%{__libtoolize} --ltdl
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	--disable-static \
	--enable-intf-lan \
	--enable-intf-lanplus \
	--enable-intf-open \
	--enable-intf-imb \
	--enable-ipmishell \
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
%doc AUTHORS COPYING README ChangeLog
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}
%{_datadir}/*
%{_mandir}/man?/*
