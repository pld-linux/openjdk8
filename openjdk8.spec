#
# Conditional build:
%bcond_with	bootstrap	# build a bootstrap version, using default jdk (icedtea8, ocacle-java8 or so)
%bcond_without	cacerts		# don't include the default CA certificates

%if %{without bootstrap}
%define		use_jdk	openjdk8
%endif

%ifarch %{ix86} %{x8664} sparc ppc64 ppc64le %{arm} aarch64
%define		with_jfr	1
%endif

# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 52.0

%define	ver_u	362

Summary:	Open-source implementation of the Java Platform, Standard Edition
Summary(pl.UTF-8):	Wolnoźródłowa implementacja Java 8 SE
Name:		openjdk8
Version:	1.8.0.%{ver_u}
Release:	1
Epoch:		1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	https://github.com/openjdk/jdk8u/archive/jdk8u%{ver_u}-ga/%{name}-%{version}.tar.gz
# Source0-md5:	2a045aa1e95099c0ea2666e4a7719376
Source1:	https://github.com/openjdk/aarch32-port-jdk8u/archive/jdk8u%{ver_u}-ga-aarch32-20230119/%{name}-aarch32-%{version}.tar.gz
# Source1-md5:	e3d9d29cb7bbc13524e6822d06b29918
Source2:	make-cacerts.sh
Patch0:		adjust-mflags.patch
Patch1:		format_strings.patch
Patch2:		CompileDemos.patch
Patch3:		libpath.patch
Patch4:		system-libjpeg.patch
Patch5:		system-libpng.patch
Patch6:		system-lcms.patch
Patch7:		system-pcsclite.patch
Patch8:		x32.patch
Patch9:		gcc11.patch
Patch10:	link-with-as-needed.patch
Patch12:	atomic.patch
Patch13:	hotspot-disable-werror.patch
Patch14:	ignore-java-options.patch
Patch15:	default-assumemp.patch
URL:		http://openjdk.java.net/
BuildRequires:	/usr/bin/jar
BuildRequires:	alsa-lib-devel
BuildRequires:	ant
BuildRequires:	autoconf
BuildRequires:	bash
%{?with_cacerts:BuildRequires:	ca-certificates-update}
BuildRequires:	cups-devel
BuildRequires:	elfutils-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.3
BuildRequires:	gawk
BuildRequires:	giflib-devel >= 5.1
BuildRequires:	glibc-misc
%buildrequires_jdk
BuildRequires:	lcms2-devel
%ifarch %{arm}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	lsb-release
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.557
BuildRequires:	unzip
BuildRequires:	util-linux
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-proto-printproto-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	zip
BuildRequires:	zlib-devel
Requires:	%{name}-appletviewer = %{epoch}:%{version}-%{release}
Requires:	%{name}-jdk = %{epoch}:%{version}-%{release}
Suggests:	%{name}-jre-X11 = %{epoch}:%{version}-%{release}
Suggests:	icedtea-web
Obsoletes:	icedtea6
Obsoletes:	icedtea7
Obsoletes:	icedtea8
Obsoletes:	java-gcj-compat
Obsoletes:	java-gcj-compat-devel
Obsoletes:	java-sun
Obsoletes:	java-sun-demos
Obsoletes:	java-sun-jre
Obsoletes:	java-sun-jre-X11
Obsoletes:	java-sun-jre-alsa
Obsoletes:	java-sun-jre-jdbc
Obsoletes:	java-sun-tools
Obsoletes:	java5-sun
Obsoletes:	java5-sun-jre
Obsoletes:	java5-sun-jre-X11
Obsoletes:	java5-sun-jre-jdbc
Obsoletes:	java5-sun-tools
Obsoletes:	oracle-java7
Obsoletes:	oracle-java7-jre
Obsoletes:	oracle-java7-jre-X11
Obsoletes:	oracle-java7-jre-alsa
Obsoletes:	oracle-java7-jre-jdbc
Obsoletes:	oracle-java7-tools
Obsoletes:	oracle-java8
Obsoletes:	oracle-java8-jre
Obsoletes:	oracle-java8-jre-X11
Obsoletes:	oracle-java8-jre-alsa
Obsoletes:	oracle-java8-jre-jdbc
Obsoletes:	oracle-java8-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dstreldir	%{name}-%{version}
%define		dstdir		%{_jvmdir}/%{dstreldir}
%define		jrereldir	%{dstreldir}/jre
%define		jredir		%{_jvmdir}/%{jrereldir}
%define		jvmjardir	%{_jvmjardir}/%{name}-%{version}

%ifarch %{x8664}
%define		jre_arch	amd64
%endif
%ifarch %{ix86}
%define		jre_arch	i386
%endif
%ifarch x32
%define		jre_arch	x32
%endif
%ifarch aarch64
%define		jre_arch	aarch64
%endif
%ifarch %{arm}
%define		jre_arch	aarch32
%endif

%ifarch %{arm}
%define		jvm_type	client
%else
%define		jvm_type	server
%endif

# to break artificial subpackage dependency loops
%define		_noautoreq	'libmawt.so' java\\\\(ClassDataVersion\\\\)

%description
Open-source implementation of the Java Platform, Standard Edition.

This is a meta-package which provides, by its dependencies, all the
OpenJDK components including the OpenJDK, Java 8 developement kit and
runtime environment.

%description -l pl.UTF-8
Wolnoźródłowa implementacja Java 8 SE.

To jest meta-pakiet, który, za pośrednictwem zależności, dostarcza
wszystkie komponenty OpenJDK, w tym środowisko programistyczne
(OpenJDK) i uruchomieniowe (JRE).

%package jdk
Summary:	OpenJDK - software development kit
Summary(pl.UTF-8):	OpenJDK - środowisko programistyczne
Group:		Development/Languages/Java
Requires:	%{name}-jar = %{epoch}:%{version}-%{release}
Requires:	%{name}-jdk-base = %{epoch}:%{version}-%{release}
Requires:	%{name}-jre = %{epoch}:%{version}-%{release}
Provides:	j2sdk = %{version}
Provides:	jdk = %{version}
Obsoletes:	blackdown-java-sdk
Obsoletes:	ibm-java
Obsoletes:	icedtea6-jdk
Obsoletes:	icedtea7-jdk
Obsoletes:	icedtea8-jdk
Obsoletes:	java-blackdown
Obsoletes:	java-gcj-compat-devel
Obsoletes:	java-sun
Obsoletes:	java5-sun
Obsoletes:	jdk
Obsoletes:	kaffe
Obsoletes:	oracle-java7
Obsoletes:	oracle-java8

%description jdk
This package symlinks OpenJDK development tools provided by
%{name}-jdk-base to system-wide directories like %{_bindir}, making
OpenJDK the default JDK.

%description jdk -l pl.UTF-8
Ten pakiet tworzy symboliczne dowiązania do narzędzi programistycznych
OpenJDK, dostarczanych przez pakiet %{name}-jdk-base, w standardowych
systemowych ścieżkach takich jak %{_bindir}, sprawiając tym samym, że
OpenJDK staje się domyślnym JDK w systemie.

%package jdk-base
Summary:	OpenJDK - software development kit
Summary(pl.UTF-8):	Kod OpenJDK - środowisko programistyczne
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{epoch}:%{version}-%{release}
Requires:	jpackage-utils >= 0:1.7.5-8
Provides:	jdk(%{name})

%description jdk-base
OpenJDK development tools built using free software only.

%description jdk-base -l pl.UTF-8
OpenJDK skompilowane wyłącznie przy użyciu wolnego oprogramowania.

%package jre
Summary:	OpenJDK - runtime environment
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{epoch}:%{version}-%{release}
Requires:	nss >= 1:3.13.4
# Require zoneinfo data provided by java-tzdata subpackage.
Requires:	java-tzdata
Provides:	java
Provides:	java(ClassDataVersion) = %{_classdataversion}
Provides:	java(jaas) = %{version}
Provides:	java(jaf) = 1.1.1
Provides:	java(jaxp) = 1.3
Provides:	java(jaxp_parser_impl)
Provides:	java(jce) = %{version}
Provides:	java(jdbc-stdext) = %{version}
Provides:	java(jdbc-stdext) = 3.0
Provides:	java(jmx) = 1.4
Provides:	java(jndi) = %{version}
Provides:	java(jsse) = %{version}
Provides:	java1.4
Provides:	jre = %{version}
Obsoletes:	icedtea6-jre
Obsoletes:	icedtea7-jre
Obsoletes:	icedtea8-jre
Obsoletes:	jaas
Obsoletes:	jaf
Obsoletes:	java-gcj-compat
Obsoletes:	java-jaxp
Obsoletes:	java-jdbc-stdext
Obsoletes:	java-sun-jre
Obsoletes:	java5-sun-jre
Obsoletes:	jce
Obsoletes:	jdbc-stdext
Obsoletes:	jmx
Obsoletes:	jndi
Obsoletes:	jre
Obsoletes:	jsse
Obsoletes:	oracle-java7-jre
Obsoletes:	oracle-java8-jre

%description jre
This package symlinks OpenJDK runtime environment tools provided by
%{name}-jre-base to system-wide directories like %{_bindir}, making
OpenJDK the default JRE.

%description jre -l pl.UTF-8
Ten pakiet tworzy symboliczne dowiązania do środowiska
uruchomieniowego OpenJDK, dostarczanych przez pakiet %{name}-jre-base,
w standardowych systemowych ścieżkach takich jak %{_bindir},
sprawiając tym samym, że OpenJDK staje się domyślnym JRE w systemie.

%package jre-X11
Summary:	OpenJDK - runtime environment - X11 support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa X11
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{epoch}:%{version}-%{release}
Requires:	%{name}-jre-base-X11 = %{epoch}:%{version}-%{release}
Provides:	jre-X11 = %{version}
Obsoletes:	icedtea6-jre-X11
Obsoletes:	icedtea7-jre-X11
Obsoletes:	icedtea8-jre-X11
Obsoletes:	java-sun-jre-X11
Obsoletes:	oracle-java7-jre-X11
Obsoletes:	oracle-java8-jre-X11

%description jre-X11
X11 support for OpenJDK runtime environment built using free software
only.

%description jre-X11 -l pl.UTF-8
Biblioteki X11 dla środowiska OpenJDK zbudowany wyłocznie przy uzyciu
wolnego oprogramowania.

%package jre-base
Summary:	OpenJDK - runtime environment
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe
Group:		Development/Languages/Java
Requires:	jpackage-utils >= 0:1.7.5-8
Provides:	jre(%{name})

%description jre-base
OpenJDK runtime environment built using free software only.

%description jre-base -l pl.UTF-8
Środowisko uruchomieniowe OpenJDK zbudowany wyłącznie przy użyciu
wolnego oprogramowania.

%package jre-base-X11
Summary:	OpenJDK - runtime environment - X11 support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa X11
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{epoch}:%{version}-%{release}
Requires:	%{name}-jre-base-freetype = %{epoch}:%{version}-%{release}

%description jre-base-X11
X11 support for OpenJDK runtime environment built using free software
only.

%description jre-base-X11 -l pl.UTF-8
Biblioteki X11 dla środowiska OpenJDK zbudowany wyłocznie przy uzyciu
wolnego oprogramowania.

%package jre-base-alsa
Summary:	OpenJDK - runtime environment - ALSA support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa ALSA
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{epoch}:%{version}-%{release}

%description jre-base-alsa
ALSA sound support for OpenJDK runtime environment build using free
software only.

%description jre-base-alsa -l pl.UTF-8
Biblioteki ALSA rozszerzające środowisko OpenJDK o obsługę dźwięku
zbudowane przy uzyciu wyłącznie wolnego oprogramowania.

%package jre-base-freetype
Summary:	OpenJDK - runtime environment - font support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa fontów
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{epoch}:%{version}-%{release}

%description jre-base-freetype
Font handling library for OpenJDK runtime environment built using free
software only.

%description jre-base-freetype -l pl.UTF-8
Biblioteki obsługi czcionek dla OpenJDK zbudowane wyłącznie przy
użyciu wolnego oprogramowania.

%package jre-base-gtk
Summary:	OpenJDK - runtime environment - GTK support
Summary(pl.UTF-8):	OpenJDK - środowisko uruchomieniowe - obsługa GTK
Group:		Development/Languages/Java
Requires:	%{name}-jre-base = %{epoch}:%{version}-%{release}

%description jre-base-gtk
GTK support for OpenJDK runtime environment.

%description jre-base-gtk -l pl.UTF-8
Biblioteki GTK dla OpenJDK.

%package jar
Summary:	OpenJDK - JAR tool
Summary(pl.UTF-8):	OpenJDK - narzędzie JAR
Group:		Development/Languages/Java
Requires:	%{name}-jdk-base = %{epoch}:%{version}-%{release}
Provides:	jar
Obsoletes:	fastjar
Obsoletes:	icedtea6-jar
Obsoletes:	icedtea7-jar
Obsoletes:	icedtea8-jar
Obsoletes:	jar

%description jar
JAR tool from OpenJDK built using free software only.

JAR is an archiver used to merge Java classes into a single library.

%description jar -l pl.UTF-8
Narzędzie jar z OpenJDK zbudowane przy uzyciu wyłącznie wolnego
oprogramowania.

JAR jest narzędziem pozwalającym wykonywać podstawowe operacje na
archiwach javy .jar takie jak na przykład tworzenie lub rozpakowywanie
archiwów.

%package appletviewer
Summary:	OpenJDK - appletviewer tool
Summary(pl.UTF-8):	OpenJDK - narzędzie appletviewer
Group:		Development/Languages/Java
Requires:	%{name}-jdk-base = %{epoch}:%{version}-%{release}
Requires:	%{name}-jre-X11 = %{epoch}:%{version}-%{release}
Obsoletes:	icedtea6-appletviewer
Obsoletes:	icedtea7-appletviewer
Obsoletes:	icedtea8-appletviewer
Obsoletes:	java-sun-appletviewer
Obsoletes:	oracle-java7-appletviewer
Obsoletes:	oracle-java8-appletviewer

%description appletviewer
Appletviewer from OpenJDK build using free software only.

%description appletviewer -l pl.UTF-8
Appletviewer pozwala uruchamiać aplety javy niezależnie od
przeglądarki www. Ten appletviewer pochodzi z zestawu narzędzi OpenJDK
i został zbudowany wyłącznie przy użyciu wolnego oprogramowania.

%package jdk-sources
Summary:	OpenJDK - sources
Summary(pl.UTF-8):	OpenJDK - kod źródłowy
Group:		Documentation
BuildArch:	noarch

%description jdk-sources
Source code for the OpenJDK development kit and Java standard library.

%description jdk-sources -l pl.UTF-8
Kod źródłowy narzędzi programistycznych OpenJDK oraz standardowej
biblioteki Javy.

%package examples
Summary:	OpenJDK - examples
Summary(pl.UTF-8):	OpenJDK - przykłady
Group:		Documentation
BuildArch:	noarch

%description examples
Code examples for OpenJDK.

%description examples -l pl.UTF-8
Przykłady dla OpenJDK.

%prep
%setup -q -c -T
%ifarch %{arm}
tar xf %{SOURCE1} --strip-components=1
%else
tar xf %{SOURCE0} --strip-components=1
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%ifarch %{arm}
%patch12 -p1
%endif
%patch13 -p1
%patch14 -p1
%patch15 -p1

%build
# Make sure we have /proc mounted - otherwise idlc will fail later.
if [ ! -f /proc/self/stat ]; then
	echo "You need to have /proc mounted in order to build this package!"
	exit 1
fi

unset JAVA_HOME
unset CLASSPATH

# force locking irrespective of cpu count determined based on /proc and /sys contents
# https://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2021-November/026415.html
export _JAVA_OPTIONS=-XX:+AssumeMP

mkdir -p build-bin
export PATH="$(pwd)/build-bin:$PATH"

cd common/autoconf
%{__rm} generated-configure.sh
%{__autoconf} -o generated-configure.sh
cd ../..

export SHELL=/bin/bash

chmod a+x configure

# disable-debug-symbols so openjdk debuginfo handling won't conflict with ours
%configure \
%ifarch x32
	--with-jvm-variants=zero \
%else
	--with-jvm-variants=%{jvm_type} \
%endif
	--with-boot-jdk="%{java_home}" \
	--with-extra-cflags="%{rpmcppflags} %{rpmcflags}" \
	--with-extra-cxxflags="%{rpmcppflags} %{rpmcxxflags}" \
	--with-extra-ldflags="%{rpmldflags}" \
	--with-native-debug-symbols=none \
	--with-jobs="%{__jobs}" \
	--with-giflib=system \
	--with-libjpeg=system \
	--with-libpng=system \
	--with-lcms=system \
	--with-libpcsclite=system \
	--with-zlib=system \
	--with-update-version="%{ver_u}" \
	--with-build-number="%{release}" \
	--with-milestone="ga" \
	--with-vendor-name="PLD-Linux" \
	--with-vendor-url="https://www.pld-linux.org" \
	--with-vendor-bug-url="https://bugs.pld-linux.org" \
	--with-vendor-vm-bug-url="https://bugs.openjdk.java.net"

specdir="$(dirname build/*-release/spec.gmk)"
cat > $specdir/custom-spec.gmk <<EOF
# OpenJDK build system depends on bash
SHELL=/bin/bash
EOF
[ -L tmp-bin ] || ln -s "$specdir/jdk/bin" tmp-bin

%{__make} -j1 images \
	SCTP_WERROR= \
	LOG=debug \
	# these are normally set when --disable-debug-symbols is not used \
	LIBMANAGEMENT_OPTIMIZATION=LOW \
	LIBHPROF_OPTIMIZATION=LOW \
	LIBVERIFY_OPTIMIZATION=LOW

# smoke test
tmp-bin/java -version

%{?with_cacerts:%{__sh} %{SOURCE2}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{dstdir},%{_mandir}/ja} \
	$RPM_BUILD_ROOT{%{jvmjardir},%{_examplesdir}/%{name}-%{version},%{_javasrcdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# install the 'JDK image', it contains the JRE too
cp -a build/*-release/images/j2sdk-image/* $RPM_BUILD_ROOT%{dstdir}

find $RPM_BUILD_ROOT%{dstdir} -name '*.diz' -delete

# convenience symlinks without version number
ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}
ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}-jre

ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/java

# move JDK sources and demo to %{_prefix}/src
%{__mv} $RPM_BUILD_ROOT%{dstdir}/demo $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__mv} $RPM_BUILD_ROOT%{dstdir}/sample $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__mv} $RPM_BUILD_ROOT%{dstdir}/src.zip $RPM_BUILD_ROOT%{_javasrcdir}/%{name}-jdk.zip

# move manual pages to its place
%{__mv} $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8/man1 $RPM_BUILD_ROOT%{_mandir}/ja/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man/ja_JP.UTF-8
%{__rm} $RPM_BUILD_ROOT%{dstdir}/man/ja
%{__mv} $RPM_BUILD_ROOT%{dstdir}/man/man1 $RPM_BUILD_ROOT%{_mandir}/man1
rmdir $RPM_BUILD_ROOT%{dstdir}/man

# replace duplicates with symlinks, link to %{_bindir}
for path in $RPM_BUILD_ROOT%{dstdir}/bin/*; do
	filename=$(basename $path)
	if [ -e "$RPM_BUILD_ROOT%{jredir}/bin/$filename" ] && [ ! -L "$RPM_BUILD_ROOT%{jredir}/bin/$filename" ]; then
		%{__rm} "$path"
		ln -s "%{jredir}/bin/$filename" "$path"
	fi
	ln -sf "%{dstdir}/bin/$filename" $RPM_BUILD_ROOT%{_bindir}
done

ln -sf  "%{jredir}/bin/java" $RPM_BUILD_ROOT%{_bindir}

%{__rm} $RPM_BUILD_ROOT%{dstdir}/lib/%{jre_arch}/{libjawt.so,jli/libjli.so}
ln -s "%{jredir}/lib/%{jre_arch}/jli/libjli.so" "$RPM_BUILD_ROOT%{dstdir}/lib/%{jre_arch}/jli"
ln -s "%{jredir}/lib/%{jre_arch}/libjawt.so" "$RPM_BUILD_ROOT%{dstdir}/lib/%{jre_arch}"

# keep configuration in %{_sysconfdir} (not all *.properties go there)
for config in management security \
		logging.properties net.properties sound.properties; do

	mv $RPM_BUILD_ROOT%{jredir}/lib/$config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$config
	ln -s %{_sysconfdir}/%{name}/$config $RPM_BUILD_ROOT%{jredir}/lib/$config
done

%{?with_cacerts:install cacerts $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/security}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README

%files jdk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/extcheck
%attr(755,root,root) %{_bindir}/idlj
%attr(755,root,root) %{_bindir}/jarsigner
%attr(755,root,root) %{_bindir}/java-rmi.cgi
%attr(755,root,root) %{_bindir}/javac
%attr(755,root,root) %{_bindir}/javadoc
%attr(755,root,root) %{_bindir}/javah
%attr(755,root,root) %{_bindir}/javap
%attr(755,root,root) %{_bindir}/jcmd
%attr(755,root,root) %{_bindir}/jconsole
%attr(755,root,root) %{_bindir}/jdb
%attr(755,root,root) %{_bindir}/jdeps
%attr(755,root,root) %{_bindir}/jhat
%attr(755,root,root) %{_bindir}/jinfo
%attr(755,root,root) %{_bindir}/jjs
%attr(755,root,root) %{_bindir}/jmap
%attr(755,root,root) %{_bindir}/jps
%attr(755,root,root) %{_bindir}/jrunscript
%attr(755,root,root) %{_bindir}/jsadebugd
%attr(755,root,root) %{_bindir}/jstack
%attr(755,root,root) %{_bindir}/jstat
%attr(755,root,root) %{_bindir}/jstatd
%attr(755,root,root) %{_bindir}/native2ascii
%attr(755,root,root) %{_bindir}/rmic
%attr(755,root,root) %{_bindir}/schemagen
%attr(755,root,root) %{_bindir}/serialver
%attr(755,root,root) %{_bindir}/wsgen
%attr(755,root,root) %{_bindir}/wsimport
%attr(755,root,root) %{_bindir}/xjc
%{_mandir}/man1/extcheck.1*
%{_mandir}/man1/idlj.1*
%{_mandir}/man1/jarsigner.1*
%{_mandir}/man1/javac.1*
%{_mandir}/man1/javadoc.1*
%{_mandir}/man1/javah.1*
%{_mandir}/man1/javap.1*
%{_mandir}/man1/jcmd.1*
%{_mandir}/man1/jconsole.1*
%{_mandir}/man1/jdb.1*
%{_mandir}/man1/jdeps.1*
%{_mandir}/man1/jhat.1*
%{_mandir}/man1/jinfo.1*
%{_mandir}/man1/jjs.1*
%{_mandir}/man1/jmap.1*
%{_mandir}/man1/jps.1*
%{_mandir}/man1/jrunscript.1*
%{_mandir}/man1/jsadebugd.1*
%{_mandir}/man1/jstack.1*
%{_mandir}/man1/jstat.1*
%{_mandir}/man1/jstatd.1*
%{_mandir}/man1/native2ascii.1*
%{_mandir}/man1/schemagen.1*
%{_mandir}/man1/serialver.1*
%{_mandir}/man1/rmic.1*
%{_mandir}/man1/wsgen.1*
%{_mandir}/man1/wsimport.1*
%{_mandir}/man1/xjc.1*
%lang(ja) %{_mandir}/ja/man1/extcheck.1*
%lang(ja) %{_mandir}/ja/man1/idlj.1*
%lang(ja) %{_mandir}/ja/man1/jarsigner.1*
%lang(ja) %{_mandir}/ja/man1/javac.1*
%lang(ja) %{_mandir}/ja/man1/javadoc.1*
%lang(ja) %{_mandir}/ja/man1/javah.1*
%lang(ja) %{_mandir}/ja/man1/javap.1*
%lang(ja) %{_mandir}/ja/man1/jcmd.1*
%lang(ja) %{_mandir}/ja/man1/jconsole.1*
%lang(ja) %{_mandir}/ja/man1/jdb.1*
%lang(ja) %{_mandir}/ja/man1/jdeps.1*
%lang(ja) %{_mandir}/ja/man1/jhat.1*
%lang(ja) %{_mandir}/ja/man1/jinfo.1*
%lang(ja) %{_mandir}/ja/man1/jjs.1*
%lang(ja) %{_mandir}/ja/man1/jmap.1*
%lang(ja) %{_mandir}/ja/man1/jps.1*
%lang(ja) %{_mandir}/ja/man1/jrunscript.1*
%lang(ja) %{_mandir}/ja/man1/jsadebugd.1*
%lang(ja) %{_mandir}/ja/man1/jstack.1*
%lang(ja) %{_mandir}/ja/man1/jstat.1*
%lang(ja) %{_mandir}/ja/man1/jstatd.1*
%lang(ja) %{_mandir}/ja/man1/native2ascii.1*
%lang(ja) %{_mandir}/ja/man1/schemagen.1*
%lang(ja) %{_mandir}/ja/man1/serialver.1*
%lang(ja) %{_mandir}/ja/man1/rmic.1*
%lang(ja) %{_mandir}/ja/man1/wsgen.1*
%lang(ja) %{_mandir}/ja/man1/wsimport.1*
%lang(ja) %{_mandir}/ja/man1/xjc.1*

%files jdk-base
%defattr(644,root,root,755)
%doc build/*-release/images/j2sdk-image/{ASSEMBLY_EXCEPTION,THIRD_PARTY_README}
%dir %{dstdir}
%{_jvmdir}/%{name}
%dir %{dstdir}/bin
%attr(755,root,root) %{dstdir}/bin/appletviewer
%attr(755,root,root) %{dstdir}/bin/extcheck
%attr(755,root,root) %{dstdir}/bin/idlj
%attr(755,root,root) %{dstdir}/bin/jar
%attr(755,root,root) %{dstdir}/bin/jarsigner
%attr(755,root,root) %{dstdir}/bin/java-rmi.cgi
%attr(755,root,root) %{dstdir}/bin/javac
%attr(755,root,root) %{dstdir}/bin/javadoc
%attr(755,root,root) %{dstdir}/bin/javah
%attr(755,root,root) %{dstdir}/bin/javap
%attr(755,root,root) %{dstdir}/bin/jconsole
%attr(755,root,root) %{dstdir}/bin/jcmd
%attr(755,root,root) %{dstdir}/bin/jdb
%attr(755,root,root) %{dstdir}/bin/jdeps
%attr(755,root,root) %{dstdir}/bin/jhat
%attr(755,root,root) %{dstdir}/bin/jinfo
%attr(755,root,root) %{dstdir}/bin/jmap
%attr(755,root,root) %{dstdir}/bin/jps
%attr(755,root,root) %{dstdir}/bin/jrunscript
%attr(755,root,root) %{dstdir}/bin/jsadebugd
%attr(755,root,root) %{dstdir}/bin/jstack
%attr(755,root,root) %{dstdir}/bin/jstat
%attr(755,root,root) %{dstdir}/bin/jstatd
%attr(755,root,root) %{dstdir}/bin/native2ascii
%attr(755,root,root) %{dstdir}/bin/rmic
%attr(755,root,root) %{dstdir}/bin/schemagen
%attr(755,root,root) %{dstdir}/bin/serialver
%attr(755,root,root) %{dstdir}/bin/wsgen
%attr(755,root,root) %{dstdir}/bin/wsimport
%attr(755,root,root) %{dstdir}/bin/xjc
%{dstdir}/include
%dir %{dstdir}/lib
%{dstdir}/lib/ct.sym
%{dstdir}/lib/dt.jar
%{dstdir}/lib/ir.idl
%{dstdir}/lib/jconsole.jar
%attr(755,root,root) %{dstdir}/lib/jexec
%{dstdir}/lib/orb.idl
%ifnarch %{arm} x32
%{dstdir}/lib/sa-jdi.jar
%endif
%{dstdir}/lib/tools.jar
%dir %{dstdir}/lib/%{jre_arch}
%dir %{dstdir}/lib/%{jre_arch}/jli
%attr(755,root,root) %{dstdir}/lib/%{jre_arch}/jli/*.so
%{?with_systemtap:%{dstdir}/tapset}

%files jre
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/clhsdb
%attr(755,root,root) %{_bindir}/java
%{?with_jfr:%attr(755,root,root) %{_bindir}/jfr}
%attr(755,root,root) %{_bindir}/keytool
%attr(755,root,root) %{_bindir}/orbd
%attr(755,root,root) %{_bindir}/pack200
%attr(755,root,root) %{_bindir}/rmid
%attr(755,root,root) %{_bindir}/rmiregistry
%attr(755,root,root) %{_bindir}/servertool
%attr(755,root,root) %{_bindir}/tnameserv
%attr(755,root,root) %{_bindir}/unpack200
%{_mandir}/man1/java.1*
%{_mandir}/man1/keytool.1*
%{_mandir}/man1/orbd.1*
%{_mandir}/man1/pack200.1*
%{_mandir}/man1/rmid.1*
%{_mandir}/man1/rmiregistry.1*
%{_mandir}/man1/servertool.1*
%{_mandir}/man1/tnameserv.1*
%{_mandir}/man1/unpack200.1*
%lang(ja) %{_mandir}/ja/man1/java.1*
%lang(ja) %{_mandir}/ja/man1/keytool.1*
%lang(ja) %{_mandir}/ja/man1/orbd.1*
%lang(ja) %{_mandir}/ja/man1/pack200.1*
%lang(ja) %{_mandir}/ja/man1/rmid.1*
%lang(ja) %{_mandir}/ja/man1/rmiregistry.1*
%lang(ja) %{_mandir}/ja/man1/servertool.1*
%lang(ja) %{_mandir}/ja/man1/tnameserv.1*
%lang(ja) %{_mandir}/ja/man1/unpack200.1*
%{_jvmdir}/java

%files jre-base
%defattr(644,root,root,755)
%doc build/*-release/images/j2sdk-image/jre/{ASSEMBLY_EXCEPTION,THIRD_PARTY_README}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%dir %{dstdir}
%{dstdir}/release
%dir %{jredir}
%{_jvmdir}/%{name}-jre
%dir %{jredir}/bin
%dir %{dstdir}/bin
%attr(755,root,root) %{dstdir}/bin/clhsdb
%attr(755,root,root) %{jredir}/bin/java
%attr(755,root,root) %{dstdir}/bin/java
%{?with_jfr:%attr(755,root,root) %{dstdir}/bin/jfr}
%attr(755,root,root) %{jredir}/bin/jjs
%attr(755,root,root) %{dstdir}/bin/jjs
%attr(755,root,root) %{jredir}/bin/keytool
%attr(755,root,root) %{dstdir}/bin/keytool
%attr(755,root,root) %{jredir}/bin/orbd
%attr(755,root,root) %{dstdir}/bin/orbd
%attr(755,root,root) %{jredir}/bin/pack200
%attr(755,root,root) %{dstdir}/bin/pack200
%attr(755,root,root) %{jredir}/bin/rmid
%attr(755,root,root) %{dstdir}/bin/rmid
%attr(755,root,root) %{jredir}/bin/rmiregistry
%attr(755,root,root) %{dstdir}/bin/rmiregistry
%attr(755,root,root) %{jredir}/bin/servertool
%attr(755,root,root) %{dstdir}/bin/servertool
%attr(755,root,root) %{jredir}/bin/tnameserv
%attr(755,root,root) %{dstdir}/bin/tnameserv
%attr(755,root,root) %{jredir}/bin/unpack200
%attr(755,root,root) %{dstdir}/bin/unpack200
%dir %{jredir}/lib
%dir %{jredir}/lib/applet
%{jredir}/lib/cmm
%{jredir}/lib/ext
%if %{with jfr}
%{jredir}/lib/jfr.jar
%dir %{jredir}/lib/jfr
%{jredir}/lib/jfr/*.jfc
%endif
%dir %{jredir}/lib/%{jre_arch}
%dir %{jredir}/lib/%{jre_arch}/jli
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/jli/*.so
%dir %{jredir}/lib/%{jre_arch}/%{jvm_type}
%{jredir}/lib/%{jre_arch}/%{jvm_type}/Xusage.txt
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/%{jvm_type}/*.so
%{jredir}/lib/%{jre_arch}/jvm.cfg
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libattach.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt_headless.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libdt_socket.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libhprof.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libinstrument.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2gss.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2pcsc.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libj2pkcs11.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjaas_unix.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjava.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsctp.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjava_crw_demo.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjavajpeg.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjavalcms.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjdwp.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsdt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsig.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsound.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libmanagement.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libmlib_image.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnet.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnio.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libnpt.so
%ifnarch %{arm} x32
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsaproc.so
%endif
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsunec.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libunpack.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libverify.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libzip.so
%{jredir}/lib/images
%{jredir}/lib/management
%{jredir}/lib/security
%{jredir}/lib/hijrah-config-umalqura.properties
%{jredir}/lib/tzdb.dat

%if %{with webstart}
%{jredir}/lib/about.jar
%{jredir}/lib/about.jnlp
%endif
%{jredir}/lib/calendars.properties
%{jredir}/lib/charsets.jar
%{jredir}/lib/classlist
%{jredir}/lib/content-types.properties
%{jredir}/lib/currency.data
%{jredir}/lib/flavormap.properties
%{jredir}/lib/jce.jar
%attr(755, root, root) %{jredir}/lib/jexec
%{jredir}/lib/jsse.jar
%{jredir}/lib/jvm.hprof.txt
%{jredir}/lib/logging.properties
%{jredir}/lib/management-agent.jar
%{jredir}/lib/meta-index
%{jredir}/lib/net.properties
%{jredir}/lib/psfont.properties.ja
%{jredir}/lib/psfontj2d.properties
%{jredir}/lib/resources.jar
%{jredir}/lib/rt.jar
%{jredir}/lib/sound.properties
%{jvmjardir}

%files jre-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hsdb
%attr(755,root,root) %{_bindir}/policytool
%{_mandir}/man1/policytool.1*
%lang(ja) %{_mandir}/ja/man1/policytool.1*

%files jre-base-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{dstdir}/bin/hsdb
%attr(755,root,root) %{jredir}/bin/policytool
%attr(755,root,root) %{dstdir}/bin/policytool
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libawt_xawt.so
%attr(755,root,root) %{dstdir}/lib/%{jre_arch}/libjawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjawt.so
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libsplashscreen.so

%files jre-base-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libjsoundalsa.so

%files jre-base-freetype
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{jre_arch}/libfontmanager.so

%files jre-base-gtk
%defattr(644,root,root,755)

%files jar
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jar
%{_mandir}/man1/jar.1*
%lang(ja) %{_mandir}/ja/man1/jar.1*

%files appletviewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/appletviewer
%{_mandir}/man1/appletviewer.1*
%lang(ja) %{_mandir}/ja/man1/appletviewer.1*

%files jdk-sources
%defattr(644,root,root,755)
%{_javasrcdir}/%{name}-jdk.zip

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
