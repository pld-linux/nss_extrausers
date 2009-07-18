Summary:	NSS module providing additional passwd, group and shadow files
Summary(pl.UTF-8):	Moduł NSS dostarczający dodatkowe pliki passwd, group i shadow
Name:		nss_extrausers
Version:	0.2
Release:	1
License:	LGPL
Group:		Base
Source0:	http://ftp.debian.org/debian/pool/main/libn/libnss-extrausers/libnss-extrausers_%{version}.orig.tar.gz
# Source0-md5:	68f13e0dd0523a77182cac165dc5491b
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-pld.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Name Service Switch (NSS) module provides additional passwd,
group and shadow files, allowing to store system accounts ie. copied
from other systems in separate files.

%description -l pl.UTF-8
Ten moduł do serwisu nazw, dostarcza dodatkowe pliki passwd, group
i shadow pozwalając na przechowywanie danych o kontach np.
przeniesionych z innego serwera w oddzielnych plikach.

%prep
%setup -q -n libnss-extrausers-%{version}
%patch0 -p1
%patch1 -p1

%build
CC="%{__cc}"
CXX="%{__cxx}"
CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcflags} -fno-implicit-templates"
LDFLAGS="%{rpmcflags} %{rpmldflags}"
export CC CXX CFLAGS CXXFLAGS LDFLAGS

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_libdir},%{_var}/lib/extrausers}
touch $RPM_BUILD_ROOT%{_var}/lib/extrausers/{passwd,group,shadow}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /%{_libdir}/*.so*
%dir %{_var}/lib/extrausers
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/extrausers/passwd
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/extrausers/group
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/extrausers/shadow
