Summary:	Simple command-line interface to systems that support the IPMI
Summary(pl.UTF-8):	Prosty interfejs do systemów obsługujących IPMI działający z linii poleceń
Name:		ipmitool
Version:	1.8.11
Release:	3
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmitool/%{name}-%{version}.tar.gz
# Source0-md5:	0f9b4758c2b7e8a7bafc2ead113b4bc6
Source1:	%{name}-ipmievd.init
Source2:	%{name}-ipmievd.sysconfig
URL:		http://ipmitool.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Obsoletes:	ipmitool-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IPMItool is a simple command-line interface to systems that support
the Intelligent Platform Management Interface (IPMI) v1.5 and v2.0
specification. It provides the ability to read the SDR and print
sensor values, display the contents of the SEL, print FRU information,
read and set LAN configuration parameters, and perform chassis power
control. Originally written to take advantage of IPMI-over-LAN
interfaces, it is also capable of using a system interface as provided
by a kernel device driver such as OpenIPMI.

%description -l pl.UTF-8
IPMItool to prosty, działający z linii poleceń interfejs do systemów
obsługujących specyfikację Intelligent Platform Management Interface
(IPMI) v1.5 i v2.0. Daje możliwość odczytu SDR i wypisania wartości
czujników, wyświetlenia zawartości SEL, wypisania informacji FRU,
odczytu i ustawiania parametrów konfiguracji LAN i sterowania
zasilaniem. Narzędzie napisano pierwotnie w celu wykorzystania
interfejsów IPMI-over-LAN, ale możliwe jest także używanie interfejsu
systemowego dostarczonego przez sterownik urządzenia w jądrze, taki
jak OpenIPMI.

%package ipmievd
Summary:	IPMI event daemon for sending events to syslog
Summary(pl.UTF-8):	Demon IPMI przesyłający zdarzenia do sysloga
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description ipmievd
ipmievd is a daemon which will listen for events from the BMC that are
being sent to the SEL and also log those messages to syslog.

%description ipmievd -l pl.UTF-8
ipmievd to demon, który nasłuchuje na zdarzenia z BMC, które są
wysyłane do SEL i loguje wiadomości do sysloga.

%prep
%setup -q

%build
%{__libtoolize} --ltdl
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	--disable-static \
	--enable-intf-bmc \
	--enable-intf-free \
	--enable-intf-imb \
	--enable-intf-lan \
	--enable-intf-lanplus \
	--enable-intf-lipmi \
	--enable-intf-open \
	--enable-ipmishell
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/ipmievd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ipmievd

%clean
rm -rf $RPM_BUILD_ROOT

%post ipmievd
/sbin/chkconfig --add ipmievd
%service ipmievd restart

%preun ipmievd
if [ "$1" = "0" ]; then
        %service ipmievd stop
        /sbin/chkconfig --del ipmievd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_datadir}/ipmitool
%{_mandir}/man1/*

%files ipmievd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/ipmievd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ipmievd
%{_mandir}/man8/*
