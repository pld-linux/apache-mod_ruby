%define		mod_name	mod_ruby
%define 	apxs		/usr/sbin/apxs
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_httpdconf	%{_sysconfdir}/httpd/httpd.conf
%define		_modrubyconf	%{_sysconfdir}/httpd/mod_ruby.conf
%define		_swap		/tmp/$$.swap
Summary:	Apache module: mod_ruby - embeds the Ruby interpreter into the Apache web server
Summary(pl):	Modu� do Apache'a: mod_ruby - zapewnia obs�ug� skrypt�w rubego przez serwer Apache
Name:		apache-%{mod_name}
Version:	1.0.7
Release:	0.9
Group:		Networking/Daemons
License:	GPL
Source0:	http://www.modruby.net/archive/%{mod_name}-%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		%{name}-struct.patch
URL:		http://www.modruby.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	ruby >= 1.6.4
Requires:	apache >= 1.3.3
BuildRequires:	ruby >= 1.6.4
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 1.3.3

%description
mod_ruby embeds the Ruby interpreter into the Apache web server,
allowing Ruby CGI scripts to be executed natively. These scripts will
start up much faster than without mod_ruby.

%description -l pl
mod_ruby zapewnia obs�ug� skrypt�w Ruby'ego bezpo�rednio z poziomu
Apache'a, dzi�ki czemu b�d� si� one �adowa�y znacnie szybciej ni�
gdyby by�y wowo�ywane tradycyjnie.

%prep
%setup -q -n %{mod_name}-%{version}
%patch0 -p1

%build
./configure.rb --with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildroot}
#%{__make} DESTDIR=$RPM_BUILD_ROOT install

install -d $RPM_BUILD_ROOT%{_pkglibdir}
install %{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/%{mod_name}.so

# Install the config file
install -d %{buildroot}%{_sysconfdir}/httpd/
install %{SOURCE1} $RPM_BUILD_ROOT%{_modrubyconf}

%clean
rm -rf %{buildroot}

%post
%{apxs} -e -a -n ruby %{_pkglibdir}/%{mod_name}.so 1>&2
echo "Include %{_modrubyconf}" >> %{_httpdconf}
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n ruby %{_pkglibdir}/%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi
cat %{_httpdconf} | grep -v "Include %{_modrubyconf}" > %{_swap}
mv %{_swap} %{_httpdconf}

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README.ja README.en examples doc/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/mod_ruby.conf
%attr(755,root,root) %{_pkglibdir}/*