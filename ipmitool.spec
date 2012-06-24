Summary:	Simple command-line interface to systems that support the IPMI
Summary(pl):	Prosty dzia�aj�cy z linii polece� interfejs do system�w obs�uguj�cych IPMI
Name:		ipmitool
Version:	1.8.8
Release:	1
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/ipmitool/%{name}-%{version}.tar.gz
# Source0-md5:	8ae20a7621b00148acacab5b44540f3e
Source1:	%{name}-ipmievd.init
Source2:	%{name}-ipmievd.sysconfig
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

%package ipmievd
Summary:	IPMI event daemon for sending events to syslog
Summary(pl):	Demon IPMI przesy�aj�cy zdarzenia do sysloga
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description ipmievd
ipmievd is a daemon which will listen for events from the BMC that are
being sent to the SEL and also log those messages to syslog.

%description ipmievd -l pl
ipmievd to demon, kt�ry nas�uchuje na zdarzenia z BMC, kt�re s�
wysy�ane do SEL i loguje wiadomo�ci do sysloga.

%prep
%setup -q
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
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/*

%files ipmievd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%attr(754,root,root) /etc/rc.d/init.d/ipmievd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ipmievd
