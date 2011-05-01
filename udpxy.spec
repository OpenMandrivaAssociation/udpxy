%define realversion 1.0-Chipmunk-19

Name:           udpxy
Version:        1.0.19
Release:        %mkrel 0
Summary:        UDP-to-HTTP multicast traffic relay daemon
Group:          System/Servers
License:        GPLv3+
URL:            http://sourceforge.net/projects/udpxy/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}.%{realversion}.tgz
Source1:        udpxy.init
Source2:        udpxy.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

%description
udpxy is a UDP-to-HTTP multicast traffic relay daemon:
it forwards UDP traffic from a given multicast subscription
to the requesting HTTP client.

%prep
%setup -q -n %{name}-%{realversion}

chmod a-x CHANGES
sed -i "s|CFLAGS += -W -Wall -Werror --pedantic|CFLAGS += %{optflags}|g" Makefile

%build
%make


%install
rm -rf %{buildroot}

sed -i "s|INSTALLROOT := /usr/local|INSTALLROOT := %{buildroot}/usr|g" Makefile
sed -i 's|ln -s $(INSTALLROOT)/bin/$(EXEC)|ln -s $(EXEC)|g' Makefile

%makeinstall

pushd %{buildroot}
mkdir -p .%{_sysconfdir}/sysconfig .%{_initrddir}
install -p -m755 %{SOURCE1} .%{_initrddir}/%{name}
install -p -m644 %{SOURCE2} .%{_sysconfdir}/sysconfig/%{name}
popd

%clean
rm -rf %{buildroot}


%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root,-)
%doc README CHANGES gpl.txt udpxy-manual-RU.rtf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%{_bindir}/%{name}
%{_bindir}/udpxrec
