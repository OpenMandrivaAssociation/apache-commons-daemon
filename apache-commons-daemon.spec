
%global base_name   daemon
%global short_name  commons-%{base_name}

Name:           apache-%{short_name}
Version:        1.0.7
Release:        1
Summary:        Defines API to support an alternative invocation mechanism
License:        ASL 2.0
Group:          System/Base
URL:            http://commons.apache.org/%{base_name}
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         0001-execve-path-warning.patch
Patch1:         0002-ppc64-configure.patch
Patch2:         0003-s390x-configure.patch
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  maven
BuildRequires:  apache-commons-parent
BuildRequires:  xmlto

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils


# This should go away with F-17
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} <= 1.0.1


%description
The scope of this package is to define an API in line with the current
Java Platform APIs to support an alternative invocation mechanism
which could be used instead of the public static void main(String[])
method.  This specification covers the behavior and life cycle of what
we define as Java daemons, or, in other words, non interactive
Java applications.

%package        jsvc
Summary:        Java daemon launcher
Group:          System/Base
Provides:       jsvc = %{version}-%{release}

Provides:       jakarta-%{short_name}-jsvc = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-jsvc <= 1.0.1

%description    jsvc
%{summary}.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Development/Java
Requires:       jpackage-utils
BuildArch:      noarch

Obsoletes:      jakarta-%{short_name}-javadoc <= 1.0.1

%description    javadoc
%{summary}.


%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1 -b .execve
%patch1 -p1 -b .ppc
# %%patch2 -p1 -b .s390 <- needs a rediff, or nuke it?

# remove java binaries from sources
rm -rf src/samples/build/

chmod 644 src/samples/*
cd src/native/unix
xmlto man man/jsvc.1.xml --skip-validation


%build

# build native jsvc
pushd src/native/unix
%configure --with-java=%{java_home}
# this is here because 1.0.2 archive contains old *.o
make clean
make %{?_smp_mflags}
popd

# build jars
mvn-local install javadoc:javadoc



%install

# install native jsvc
install -Dpm 755 src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}/jsvc
install -Dpm 644 src/native/unix/jsvc.1 $RPM_BUILD_ROOT%{_mandir}/man1/jsvc.1

# jars
install -Dpm 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar


# pom
install -Dpm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# following line is only for backwards compatibility. New packages
# should use proper groupid org.apache.commons and also artifactid
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE.txt PROPOSAL.html NOTICE.txt RELEASE-NOTES.txt src/samples
%doc src/docs/*
%{_javadir}/*
%{_mavenpomdir}/JPP-%{short_name}.pom
%{_mavendepmapfragdir}/*


%files jsvc
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_bindir}/jsvc
%{_mandir}/man1/jsvc.1*


%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}
%doc LICENSE.txt


