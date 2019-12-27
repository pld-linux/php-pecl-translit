#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname		translit
Summary:	%{modname} - transliterates non-latin character sets to latin
Summary(pl.UTF-8):	%{modname} - translitacja alfabetów niełacińskich do łacińskiego
Name:		%{php_name}-pecl-%{modname}
Version:	0.6.3
Release:	1
License:	BSD
Group:		Development/Languages/PHP
Source0:	https://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	4816be2da4bd063132f14cef9e1b51be
URL:		https://github.com/derickr/pecl-translit
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-devel >= 3:5.1.0
BuildRequires:	%{php_name}-iconv
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.666
%if %{with tests}
BuildRequires:	%{php_name}-pcre
%endif
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

%description -l pl.UTF-8
To rozszerzenie umożliwia transliterację tekstu ze znaków
niełacińskich (takich jak chińskie, cyrilica, greckie) na znaki
łacińskie. Oprócz transliteracji rozszerzenie zawiera także filtry na
wielkie i małe litery łacińskie, cyrylicę i greckie oraz wykonuje
specjalne formy transliteracji, takie jak konwersja ligatur takich jak
norweska ligatura "ae" na oddzielne znaki "ae" oraz normalizacja
znaków przestankowych i odstępów.

%prep
%setup -qc
mv %{modname}-%{version}/* .

cat <<'EOF' > run-tests.sh
#!/bin/sh
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
exec %{__make} test \
	PHP_EXECUTABLE=%{__php} \
	PHP_TEST_SHARED_SYSTEM_EXTENSIONS="iconv" \
	RUN_TESTS_SETTINGS="-q $*"
EOF
chmod +x run-tests.sh

%build
phpize
%configure
%{__make}

# simple module load test
%{__php} -n -q \
	-d extension_dir=modules \
	-d extension=%{php_extensiondir}/iconv.so \
	-d extension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log

%if %{with tests}
./run-tests.sh --show-diff
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
%if "%php_major_version.%php_minor_version" >= "7.4"
# order after ext-iconv
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/01_%{modname}.ini
%else
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
%endif
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/*%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
