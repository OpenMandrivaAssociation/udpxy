%define debug_package %{nil}

%global realversion 1.0.23-9

Name:           udpxy
Version:        1.0.23
Release:        1
Summary:        UDP-to-HTTP multicast traffic relay daemon
Group:          System/Servers
License:        GPLv3+
URL:            http://sourceforge.net/projects/udpxy/
Source0:        http://www.udpxy.com/download/1_23/%{name}.%{realversion}-prod.tar.gz
Source1:        udpxy.service
Source2:	udpxy-manual-RU.rtf

%description
udpxy is a UDP-to-HTTP multicast traffic relay daemon:
it forwards UDP traffic from a given multicast subscription
to the requesting HTTP client.

%prep
%setup -qn %{name}-%{realversion}
cp %{SOURCE2} .

chmod a-x CHANGES
sed -i 's|@cp $(UDPXREC)|@cp -a $(UDPXREC)|g' Makefile

%build
%make

%install
%makeinstall_std PREFIX=%{_prefix}

install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post udpxy.service

%preun
%systemd_preun udpxy.service

%postun
%systemd_postun_with_restart udpxy.service

%files
%doc README CHANGES gpl.txt udpxy-manual-RU.rtf
%{_bindir}/%{name}
%{_bindir}/udpxrec
%{_mandir}/man1/*
%{_unitdir}/%{name}.service
