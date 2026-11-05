Name:		apache-commons-daemon
Version:	1.6.1
Release:	1
Summary:	Java support classes for running applications as daemons
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-daemon/
Source0:	https://archive.apache.org/dist/commons/daemon/source/commons-daemon-%{version}-src.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(org.apache.commons:commons-parent:pom:)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-daemon --link %{name} --alias commons-daemon:commons-daemon

%description
Apache Commons Daemon provides the Java side of jsvc. This package is the
class library Tomcat ships as bin/commons-daemon.jar. The native jsvc
binary is not built here.

%prep
%setup -q -n commons-daemon-%{version}-src

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt README.md
