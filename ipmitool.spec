Summary:	Simple command-line interface to systems that support the IPMI
Summary(pl.UTF-8):	Prosty interfejs do systemów obsługujących IPMI działający z linii poleceń
Name:		ipmitool
Version:	1.8.19
%define	tagver	%(echo %{version} | tr . _)
Release:	1
License:	BSD
Group:		Applications/System
Source0:	https://github.com/ipmitool/ipmitool/archive/refs/tags/IPMITOOL_%{tagver}.tar.gz
# Source0-md5:	0aa41c99d93ce129cf00a9b8803ed8c9
Source1:	%{name}-ipmievd.init
Source2:	%{name}-ipmievd.sysconfig
Source3:	https://www.iana.org/assignments/enterprise-numbers.txt
# Source3-md5:	16631b297ca2f1d6b0481dc4957f25c8
Patch0:		no-download.patch
URL:		https://github.com/ipmitool/ipmitool
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Obsoletes:	ipmitool-devel < 1.6.0
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
%setup -q -n %{name}-IPMITOOL_1_8_19
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
	--disable-intf-bmc \
	--enable-intf-free \
	--enable-intf-imb \
	--enable-intf-lan \
	--enable-intf-lanplus \
	--enable-intf-lipmi \
	--enable-intf-open \
	--enable-ipmishell \
        --disable-registry-download
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT%{_datadir}/misc
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipmievd
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ipmievd
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/misc/enterprise-numbers

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

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
%attr(755,root,root) %{_bindir}/ipmitool
%{_datadir}/ipmitool
%{_datadir}/misc/enterprise-numbers
%{_mandir}/man1/ipmitool.1*

%files ipmievd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ipmievd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ipmievd
%attr(754,root,root) /etc/rc.d/init.d/ipmievd
%{_mandir}/man8/ipmievd.8*
