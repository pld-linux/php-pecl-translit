%define		php_name	php%{?php_suffix}
%define		status		beta
%define		modname		translit
Summary:	%{modname} - transliterates non-latin character sets to latin
Summary(pl.UTF-8):	%{modname} - translitacja alfabetów niełacińskich do łacińskiego
Name:		%{php_name}-pecl-%{modname}
Version:	0.6.2
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	https://github.com/derickr/pecl-translit/archive/RELEASE_0_6_2.tar.gz
# Source0-md5:	599a00bb624d1ebc8440698aa89585dc
URL:		https://github.com/derickr/pecl-translit
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	%{php_name}-iconv
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-translit < 0.6.1-8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allows you to transliterate text in non-latin
characters (such as Chinese, Cyrillic, Greek etc) to latin characters.
Besides the transliteration the extension also contains filters to
upper- and lowercase latin, cyrillic and greek, and perform special
forms of transliteration such as converting ligatures such as the
Norwegian "ae" ligature to separate "ae" characters and normalizing
punctuation and spacing.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
To rozszerzenie umożliwia transliterację tekstu ze znaków
niełacińskich (takich jak chińskie, cyrilica, greckie) na znaki
łacińskie. Oprócz transliteracji rozszerzenie zawiera także filtry na
wielkie i małe litery łacińskie, cyrylicę i greckie oraz wykonuje
specjalne formy transliteracji, takie jak konwersja ligatur takich jak
norweska ligatura "ae" na oddzielne znaki "ae" oraz normalizacja
znaków przestankowych i odstępów.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv pecl-translit-*/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
