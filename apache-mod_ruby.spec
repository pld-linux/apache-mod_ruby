%define		mod_name	mod_ruby
%define 	apxs		/usr/sbin/apxs
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_modrubyconf	%{_sysconfdir}/httpd/httpd.conf/70_mod_ruby.conf
%define	ruby_archdir	%(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%define ruby_rubylibdir %(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')
Summary:	Apache mod_ruby module - embeds the Ruby interpreter into the Apache web server
Summary(pl):	Modu³ Apache'a mod_ruby - zapewniaj±cy obs³ugê skryptów rubego przez serwer Apache
Name:		apache-%{mod_name}
Version:	1.2.2
Release:	1
Group:		Networking/Daemons
License:	BSD-like
Source0:	http://www.modruby.net/archive/%{mod_name}-%{version}.tar.gz
# Source0-md5:	786d740c84ec6aba73d0450b546b4642
Source1:	%{name}.conf
Patch0:		%{name}-struct.patch
URL:		http://www.modruby.net/
BuildRequires:	apache-devel >= 1.3.3
BuildRequires:	%{apxs}
BuildRequires:	ruby >= 1.6.4
Requires(post,preun):	%{apxs}
Requires:	apache >= 1.3.3
Requires:	ruby >= 1.6.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mod_ruby embeds the Ruby interpreter into the Apache web server,
allowing Ruby CGI scripts to be executed natively. These scripts will
start up much faster than without mod_ruby.

%description -l pl
mod_ruby zapewnia obs³ugê skryptów Ruby'ego bezpo¶rednio z poziomu
Apache'a, dziêki czemu bêd± siê one ³adowa³y znacnie szybciej ni¿
gdyby by³y wywo³ywane tradycyjnie.

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

install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{ruby_rubylibdir}}
install %{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/%{mod_name}.so

# Install the config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_modrubyconf}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README.en examples doc/*
%lang(ja) %doc README.ja
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/70_mod_ruby.conf
%attr(755,root,root) %{_pkglibdir}/*
%{ruby_rubylibdir}/*
