%define		mod_name	mod_ruby
%define 	apxs		/usr/sbin/apxs
Summary:	Apache mod_ruby module - embeds the Ruby interpreter into the Apache web server
Summary(pl.UTF-8):	Moduł Apache'a mod_ruby - zapewniający obsługę skryptów rubego przez serwer Apache
Name:		apache-%{mod_name}
Version:	1.2.5
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Source0:	http://www.modruby.net/archive/%{mod_name}-%{version}.tar.gz
# Source0-md5:	3c867008bd6518c1fec395d9040cd964
Source1:	%{name}.conf
Patch0:		%{name}-struct.patch
URL:		http://www.modruby.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	ruby-devel >= 1:1.6.4
Requires:	apache(modules-api) = %apache_modules_api
Requires:	ruby >= 1:1.6.4
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_ruby embeds the Ruby interpreter into the Apache web server,
allowing Ruby CGI scripts to be executed natively. These scripts will
start up much faster than without mod_ruby.

%description -l pl.UTF-8
mod_ruby zapewnia obsługę skryptów Ruby'ego bezpośrednio z poziomu
Apache'a, dzięki czemu będą się one ładowały znacznie szybciej niż
gdyby były wywoływane tradycyjnie.

%prep
%setup -q -n %{mod_name}-%{version}
%patch0 -p1

%build
./configure.rb \
	--with-apr-includes='/usr/include/apr -I/usr/include/apr-util'\
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf,%{ruby_rubylibdir}}
install %{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/%{mod_name}.so
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/70_mod_%{mod_name}.conf
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README.en examples doc/*
%lang(ja) %doc README.ja
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%{ruby_rubylibdir}/*
