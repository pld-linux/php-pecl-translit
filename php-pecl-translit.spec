%define		_modname	translit
%define		_status		beta

Summary:	%{_modname} - transliterates non-latin character sets to latin
Summary(pl):	%{_modname} - translitacja alfabetów nie³aciñskich do ³aciñskiego
Name:		php-pecl-%{_modname}
Version:	0.2
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	cd82fa5feb19a74c5a0d6bb60a9af8e3
URL:		http://pecl.php.net/package/translit/
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php-common >= 3:5.0.0
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
This extension allows you to transliterate text in non-latin
characters (such as Chinese, Cyrillic, Greek etc) to latin characters.
Besides the transliteration the extension also contains filters to
upper- and lowercase latin, cyrillic and greek, and perform special
forms of transliteration such as converting ligatures such as the
Norwegian "ae" ligature to separate "ae" characters and normalizing
punctuation and spacing.

In PECL status of this extension is: %{_status}.

%description -l pl
To rozszerzenie umo¿liwia transliteracjê tekstu ze znaków
nie³aciñskich (takich jak chiñskie, cyrilica, greckie) na znaki
³aciñskie. Oprócz transliteracji rozszerzenie zawiera tak¿e filtry
na wielkie i ma³e litery ³aciñskie, cyrylicê i greckie oraz wykonuje
specjalne formy transliteracji, takie jak konwersja ligatur takich jak
norweska ligatura "ae" na oddzielne znaki "ae" oraz normalizacja
znaków przestankowych i odstêpów.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
