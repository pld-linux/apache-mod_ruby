%define		mod_name	mod_ruby
%define 	apxs		/usr/sbin/apxs
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_httpdconf	%{_sysconfdir}/httpd/httpd.conf
%define		_modrubyconf	%{_sysconfdir}/httpd/mod_ruby.conf
Summary:	Apache mod_ruby module - embeds the Ruby interpreter into the Apache web server
Summary(pl):	Modu³ Apache'a mod_ruby - zapewniaj±cy obs³ugê skryptów rubego przez serwer Apache
Name:		apache-%{mod_name}
Version:	1.0.7
Release:	0.9
Group:		Networking/Daemons
License:	BSD-like
Source0:	http://www.modruby.net/archive/%{mod_name}-%{version}.tar.gz
# Source0-md5:	b03bb4e2fe58f6f3251a8aa168364221
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
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_pkglibdir}
install %{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/%{mod_name}.so

# Install the config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd
install %{SOURCE1} $RPM_BUILD_ROOT%{_modrubyconf}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n ruby %{_pkglibdir}/%{mod_name}.so 1>&2
if [ -f %{_httpdconf} ] && ! grep -q "^Include.*%{modrubyconf}" %{_httpdconf}; then
	echo "Include %{_modrubyconf}" >> %{_httpdconf}
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n ruby %{_pkglibdir}/%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
	umask 027
	cat %{_httpdconf} | grep -v "Include %{_modrubyconf}" > %{_httpdconf}.tmp
	mv -f %{_httpdconf}.tmp %{_httpdconf}
fi

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README.en examples doc/*
%lang(ja) %doc README.ja
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/mod_ruby.conf
%attr(755,root,root) %{_pkglibdir}/*
