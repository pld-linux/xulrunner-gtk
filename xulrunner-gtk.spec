#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)

#
%define		_realname	xulrunner
%define		_snap	20071201
%define		_rel	1
#
Summary:	XULRunner - Mozilla Runtime Environment for XUL+XPCOM applications
Summary(pl.UTF-8):	XULRunner - środowisko uruchomieniowe Mozilli dla aplikacji XUL+XPCOM
Name:		xulrunner-gtk
Version:	1.8.1.11
Release:	1.%{_snap}.%{_rel}
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications
Source0:	%{_realname}-%{version}-%{_snap}-source.tar.bz2
# Source0-md5:	7e1701a44025977413e91d3ae9483f51
Patch0:		%{_realname}-ldap-with-nss.patch
Patch1:		%{_realname}-install.patch
Patch2:		%{_realname}-pc.patch
Patch3:		%{_realname}-rpath.patch
URL:		http://developer.mozilla.org/en/docs/XULRunner
BuildRequires:	/bin/csh
BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	krb5-devel
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.4
BuildRequires:	nss-devel >= 1:3.11.3-3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	%{name}-libs = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	nspr >= 1:4.6.4
Requires:	nss >= 1:3.11.3
Provides:	xulrunner = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

# we don't want these to satisfy xulrunner-devel [???]
%define		_noautoprov	libmozjs.so libxpcom.so
# no need to require them (we have strict deps for these)
%define		_noautoreq	libgtkembedmoz.so libldap50.so libmozjs.so libprldap50.so libssldap50.so libxpcom.so libxul.so

%description
XULRunner is a Mozilla runtime package that can be used to bootstrap
XUL+XPCOM applications that are as rich as Firefox and Thunderbird. It
will provide mechanisms for installing, upgrading, and uninstalling
these applications. XULRunner will also provide libxul, a solution
which allows the embedding of Mozilla technologies in other projects
and products. Wersion without Gnome dependencies.

%description -l pl.UTF-8
XULRunner to pakiet uruchomieniowy Mozilli, którego można użyć do
uruchamiania aplikacji XUL+XPCOM, nawet takich jak Firefox czy
Thunderbird. Udostępni mechanizmy do instalowania, uaktualniania i
odinstalowywania tych aplikacji. XULRunner będzie także dostarczał
libxul - rozwiązanie umożliwiające osadzanie technologii Mozilli w
innych projektach i produktach. Wersja bez zaleznosci Gnome.

%package libs
Summary:	XULRunner shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone XULRunnera
Group:		X11/Libraries
Provides:	xulrunner-libs = %{version}-%{release}

%description libs
XULRunner shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone XULRunnera.

%package devel
Summary:	Headers for developing programs that will use XULRunner
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów używających XULRunnera
Group:		X11/Development/Libraries
Requires:	nspr-devel >= 1:4.6.4
Requires:	nss-devel >= 1:3.11.3
Requires:	xulrunner-libs = %{version}-%{release}
Provides:	xulrunner-devel = %{version}-%{release}
Obsoletes:	mozilla-devel
Obsoletes:	mozilla-firefox-devel
Obsoletes:	seamonkey-devel

%description devel
XULRunner development package.

%description devel -l pl.UTF-8
Pakiet programistyczny XULRunnera.

%prep
%setup -qc
cd mozilla

rm -rf mozilla/modules/libbz2

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd mozilla

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/xulrunner/config/mozconfig

# Options for 'configure' (same as command-line options).
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags}"
%endif
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
ac_add_options --disable-gnomevfs
ac_add_options --disable-gnomeui
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-xinerama
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-system-cairo
ac_add_options --enable-xft
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{_realname}

ac_add_options --disable-pedantic
ac_add_options --disable-xterm-updates
ac_add_options --enable-extensions="default,cookie,permissions,spellcheck"
ac_add_options --enable-ldap
ac_add_options --enable-xprint
ac_add_options --with-pthreads
ac_add_options --with-x
ac_cv_visibility_pragma=no
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla

%{__make} -C xpinstall/packager make-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{_realname} \
	PKG_SKIP_STRIP=1

install -d \
	$RPM_BUILD_ROOT%{_datadir}/%{_realname}/components \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT{%{_pkgconfigdir},%{_includedir}}

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{_realname}/chrome $RPM_BUILD_ROOT%{_datadir}/%{_realname}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{_realname}/defaults $RPM_BUILD_ROOT%{_datadir}/%{_realname}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{_realname}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{_realname}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{_realname}/res $RPM_BUILD_ROOT%{_datadir}/%{_realname}/res
ln -s ../../share/%{_realname}/chrome $RPM_BUILD_ROOT%{_libdir}/%{_realname}/chrome
ln -s ../../share/%{_realname}/defaults $RPM_BUILD_ROOT%{_libdir}/%{_realname}/defaults
ln -s ../../share/%{_realname}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{_realname}/greprefs
ln -s ../../share/%{_realname}/res $RPM_BUILD_ROOT%{_libdir}/%{_realname}/res

# files created by regxpcom
touch $RPM_BUILD_ROOT%{_libdir}/%{_realname}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{_realname}/components/xpti.dat

# header/development files
cp -rfLp dist/include	$RPM_BUILD_ROOT%{_includedir}/%{_realname}
cp -rfLp dist/idl	$RPM_BUILD_ROOT%{_includedir}/%{_realname}
cp -rfLp dist/public/ldap{,-private} $RPM_BUILD_ROOT%{_includedir}/%{_realname}
install dist/bin/regxpcom $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_libdir}/%{_realname}/xpidl $RPM_BUILD_ROOT%{_bindir}/xpidl
mv $RPM_BUILD_ROOT%{_libdir}/%{_realname}/xpt_dump $RPM_BUILD_ROOT%{_bindir}/xpt_dump
mv $RPM_BUILD_ROOT%{_libdir}/%{_realname}/xpt_link $RPM_BUILD_ROOT%{_bindir}/xpt_link

%{__make} -C build/unix install \
	DESTDIR=$RPM_BUILD_ROOT

%browser_plugins_add_browser %{_realname} -p %{_libdir}/%{_realname}/plugins

# we use system pkgs
rm $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-{nspr,nss}.pc

# rpath is used, can move to bindir
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_realname}/xulrunner
mv $RPM_BUILD_ROOT{%{_libdir}/%{_realname}/xulrunner-bin,%{_bindir}/xulrunner}
mv $RPM_BUILD_ROOT{%{_libdir}/%{_realname}/xpcshell,%{_bindir}}

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{_realname}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{_realname}/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

LD_LIBRARY_PATH=%{_libdir}/%{_realname}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} %{_libdir}/%{_realname}/regxpcom

rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/%{_realname}-chrome+xpcom-generate
%update_browser_plugins

%postun
if [ "$1" = "1" ]; then
	%{_sbindir}/%{_realname}-chrome+xpcom-generate
fi
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xulrunner
%attr(744,root,root) %{_sbindir}/%{_realname}-chrome+xpcom-generate

%dir %{_libdir}/%{_realname}/chrome
%dir %{_libdir}/%{_realname}/components
%dir %{_libdir}/%{_realname}/defaults
%dir %{_libdir}/%{_realname}/greprefs
%dir %{_libdir}/%{_realname}/plugins
%dir %{_libdir}/%{_realname}/res
%dir %{_datadir}/%{_realname}

%attr(755,root,root) %{_libdir}/%{_realname}/regxpcom

%{_browserpluginsconfdir}/browsers.d/%{_realname}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{_realname}.*.blacklist

%attr(755,root,root) %{_libdir}/%{_realname}/components/libauth.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libautoconfig.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libcookie.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libfileview.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libmozldap.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libmyspell.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libpermissions.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libpipboot.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libpipnss.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libpippki.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libspellchecker.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libsystem-pref.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libtransformiix.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libuniversalchardet.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libwebsrvcs.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libxmlextras.so
%attr(755,root,root) %{_libdir}/%{_realname}/components/libxulutil.so

%{_libdir}/%{_realname}/components/accessibility*.xpt
%{_libdir}/%{_realname}/components/alerts.xpt
%{_libdir}/%{_realname}/components/appshell.xpt
%{_libdir}/%{_realname}/components/appstartup.xpt
%{_libdir}/%{_realname}/components/autocomplete.xpt
%{_libdir}/%{_realname}/components/autoconfig.xpt
%{_libdir}/%{_realname}/components/caps.xpt
%{_libdir}/%{_realname}/components/chardet.xpt
%{_libdir}/%{_realname}/components/chrome.xpt
%{_libdir}/%{_realname}/components/commandhandler.xpt
%{_libdir}/%{_realname}/components/commandlines.xpt
%{_libdir}/%{_realname}/components/composer.xpt
%{_libdir}/%{_realname}/components/content_*.xpt
%{_libdir}/%{_realname}/components/cookie.xpt
%{_libdir}/%{_realname}/components/directory.xpt
%{_libdir}/%{_realname}/components/docshell.xpt
%{_libdir}/%{_realname}/components/dom*.xpt
%{_libdir}/%{_realname}/components/downloads.xpt
%{_libdir}/%{_realname}/components/editor.xpt
%{_libdir}/%{_realname}/components/embed_base.xpt
%{_libdir}/%{_realname}/components/extensions.xpt
%{_libdir}/%{_realname}/components/exthandler.xpt
%{_libdir}/%{_realname}/components/fastfind.xpt
%{_libdir}/%{_realname}/components/feeds.xpt
%{_libdir}/%{_realname}/components/filepicker.xpt
%{_libdir}/%{_realname}/components/find.xpt
%{_libdir}/%{_realname}/components/gfx*.xpt
%{_libdir}/%{_realname}/components/history.xpt
%{_libdir}/%{_realname}/components/htmlparser.xpt
%{_libdir}/%{_realname}/components/imglib2.xpt
%{_libdir}/%{_realname}/components/inspector.xpt
%{_libdir}/%{_realname}/components/intl.xpt
%{_libdir}/%{_realname}/components/jar.xpt
%{_libdir}/%{_realname}/components/js*.xpt
%{_libdir}/%{_realname}/components/layout*.xpt
%{_libdir}/%{_realname}/components/locale.xpt
%{_libdir}/%{_realname}/components/lwbrk.xpt
%{_libdir}/%{_realname}/components/mimetype.xpt
%{_libdir}/%{_realname}/components/moz*.xpt
%{_libdir}/%{_realname}/components/necko*.xpt
%{_libdir}/%{_realname}/components/oji.xpt
%{_libdir}/%{_realname}/components/passwordmgr.xpt
%{_libdir}/%{_realname}/components/pipboot.xpt
%{_libdir}/%{_realname}/components/pipnss.xpt
%{_libdir}/%{_realname}/components/pippki.xpt
%{_libdir}/%{_realname}/components/plugin.xpt
%{_libdir}/%{_realname}/components/pref.xpt
%{_libdir}/%{_realname}/components/prefetch.xpt
%{_libdir}/%{_realname}/components/profile.xpt
%{_libdir}/%{_realname}/components/progressDlg.xpt
%{_libdir}/%{_realname}/components/proxyObjInst.xpt
%{_libdir}/%{_realname}/components/rdf.xpt
%{_libdir}/%{_realname}/components/satchel.xpt
%{_libdir}/%{_realname}/components/saxparser.xpt
%{_libdir}/%{_realname}/components/shistory.xpt
%{_libdir}/%{_realname}/components/spellchecker.xpt
%{_libdir}/%{_realname}/components/storage.xpt
%{_libdir}/%{_realname}/components/toolkitprofile.xpt
%{_libdir}/%{_realname}/components/toolkitremote.xpt
%{_libdir}/%{_realname}/components/txmgr.xpt
%{_libdir}/%{_realname}/components/txtsvc.xpt
%{_libdir}/%{_realname}/components/uconv.xpt
%{_libdir}/%{_realname}/components/unicharutil.xpt
%{_libdir}/%{_realname}/components/update.xpt
%{_libdir}/%{_realname}/components/uriloader.xpt
%{_libdir}/%{_realname}/components/urlformatter.xpt
%{_libdir}/%{_realname}/components/webBrowser_core.xpt
%{_libdir}/%{_realname}/components/webbrowserpersist.xpt
%{_libdir}/%{_realname}/components/webshell_idls.xpt
%{_libdir}/%{_realname}/components/websrvcs.xpt
%{_libdir}/%{_realname}/components/widget.xpt
%{_libdir}/%{_realname}/components/windowds.xpt
%{_libdir}/%{_realname}/components/windowwatcher.xpt
%{_libdir}/%{_realname}/components/x*.xpt

%{_libdir}/%{_realname}/components/FeedProcessor.js
%{_libdir}/%{_realname}/components/jsconsole-clhandler.js
%{_libdir}/%{_realname}/components/nsCloseAllWindows.js
%{_libdir}/%{_realname}/components/nsDefaultCLH.js
%{_libdir}/%{_realname}/components/nsDictionary.js
%{_libdir}/%{_realname}/components/nsExtensionManager.js
%{_libdir}/%{_realname}/components/nsFilePicker.js
%{_libdir}/%{_realname}/components/nsHelperAppDlg.js
%{_libdir}/%{_realname}/components/nsInterfaceInfoToIDL.js
%{_libdir}/%{_realname}/components/nsKillAll.js
%{_libdir}/%{_realname}/components/nsProgressDialog.js
%{_libdir}/%{_realname}/components/nsProxyAutoConfig.js
%{_libdir}/%{_realname}/components/nsResetPref.js
%{_libdir}/%{_realname}/components/nsUpdateService.js
%{_libdir}/%{_realname}/components/nsURLFormatter.js
%{_libdir}/%{_realname}/components/nsXmlRpcClient.js
%{_libdir}/%{_realname}/components/nsXULAppInstall.js

# do not use *.dat here, so check-files can catch any new files
# (and they won't be just silently placed empty in rpm)
%ghost %{_libdir}/%{_realname}/components/compreg.dat
%ghost %{_libdir}/%{_realname}/components/xpti.dat

%dir %{_datadir}/%{_realname}/chrome
%{_datadir}/%{_realname}/chrome/classic.jar
%{_datadir}/%{_realname}/chrome/classic.manifest
%{_datadir}/%{_realname}/chrome/comm.jar
%{_datadir}/%{_realname}/chrome/comm.manifest
%{_datadir}/%{_realname}/chrome/en-US.jar
%{_datadir}/%{_realname}/chrome/en-US.manifest
%{_datadir}/%{_realname}/chrome/pippki.jar
%{_datadir}/%{_realname}/chrome/pippki.manifest
%{_datadir}/%{_realname}/chrome/toolkit.jar
%{_datadir}/%{_realname}/chrome/toolkit.manifest

%{_datadir}/%{_realname}/chrome/chromelist.txt
#%ghost %{_datadir}/%{_realname}/chrome/installed-chrome.txt

%{_datadir}/%{_realname}/defaults
%{_datadir}/%{_realname}/greprefs
%{_datadir}/%{_realname}/res

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{_realname}
%attr(755,root,root) %{_libdir}/%{_realname}/libgtkembedmoz.so
%attr(755,root,root) %{_libdir}/%{_realname}/libldap50.so
%attr(755,root,root) %{_libdir}/%{_realname}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{_realname}/libprldap50.so
%attr(755,root,root) %{_libdir}/%{_realname}/libssldap50.so
%attr(755,root,root) %{_libdir}/%{_realname}/libxpcom.so
%attr(755,root,root) %{_libdir}/%{_realname}/libxul.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/regxpcom
%attr(755,root,root) %{_bindir}/xpcshell
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%attr(755,root,root) %{_bindir}/xulrunner-config
%attr(755,root,root) %{_libdir}/%{_realname}/xulrunner-stub
%{_includedir}/%{_realname}
%{_pkgconfigdir}/*
