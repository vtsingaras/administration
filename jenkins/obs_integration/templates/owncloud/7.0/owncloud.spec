#
# spec file for package owncloud
#
# Copyright (c) 2012-2014 ownCloud, Inc.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes, issues or comments via http://github.com/owncloud/
#

#
%if 0%{?suse_version}
%define apache_serverroot /srv/www/htdocs
%define apache_confdir /etc/apache2/conf.d
%define apache_user wwwrun
%define apache_group www
%else
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
%define apache_serverroot /var/www/html
%define apache_confdir /etc/httpd/conf.d
%define apache_user apache
%define apache_group apache
%define __jar_repack 0
%else
%define apache_serverroot /var/www
%define apache_confdir /etc/httpd/conf.d
%define apache_user www
%define apache_group www
%endif
%endif

%define oc_user 	%{apache_user}
%define oc_dir  	%{apache_serverroot}/%{name}
%define ocphp_bin	/usr/bin

%if 0%{?rhel} == 600 || 0%{?rhel_version} == 600 || 0%{?centos_version} == 600
%define statedir	/var/run
%else
%define statedir	/run
%endif

Name:           owncloud

# Downloaded from http://download.owncloud.org/owncloud-7.0.0.tar.bz2
# Downloaded from http://download.owncloud.org/community/owncloud-7.0.1.tar.bz2

## define prerelease %nil, if this is *not* a prerelease.
%define prerelease [% PRERELEASE %]
%define base_version [% VERSION %]

%if 0%{?centos_version} == 600 || 0%{?fedora_version} || "%{prerelease}" == ""
# For beta and rc versions we use the ~ notation, as documented in
# http://en.opensuse.org/openSUSE:Package_naming_guidelines
Version:       	%{base_version}
%if "%{prerelease}" == ""
Release:        0
%else
Release:       	0.<CI_CNT>.<B_CNT>.%{prerelease}
%endif
%else
Version:       	%{base_version}~%{prerelease}
Release:        0
%endif

Source0:        [% SOURCE_TAR_URL %]
Source1:        apache_secure_data
Source2:        README
Source3:        README.SELinux
Source4:        robots.txt
Url:            http://www.owncloud.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Summary:        The ownCloud Server - Private file sync and share server
License:        AGPL-3.0 and MIT
Group:          Productivity/Networking/Web/Utilities

%if 0%{?fedora_version} || 0%{?rhel_version} >= 600 || 0%{?centos_version} >= 600
Requires:       httpd sqlite php php-json php-mbstring php-process php-xml php-zip php-pdo php-gd
%if 0%{?rhel_version} > 600 || 0%{?centos_version} > 600
# OBS for centos 6: error: unpacking of archive failed on file /var/run/httpd: cpio: mkdir failed
BuildRequires:  httpd
%endif
%endif

%if 0%{?fedora_version}
# These two are missing at CentOS/RHEL: do we really need them? 
Requires:       php-pear-Net-Curl php-pear-MDB2-Driver-mysqli 
BuildRequires:  php-pear-Net-Curl php-pear-MDB2-Driver-mysqli
%endif

%if 0%{?rhel_version} == 5 || 0%{?centos_version} == 5
Requires:       httpd sqlite php53 >= 5.3.3 php53-json php53-mbstring php53-process php53-pear-Net-Curl php53-gd php53-pear-MDB2-Driver-mysqli php53-xml php53-zip
%endif
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
# https://github.com/owncloud/core/issues/11576
# at CentOS6, we need policycoreutils-python for semanage.
Requires:	policycoreutils-python
BuildRequires:	policycoreutils-python
%endif

%if 0%{?suse_version}
BuildRequires: 	fdupes
%if 0%{?suse_version} != 1110
# For all SUSEs except SLES 11
Requires:       apache2 apache2-mod_php5 php5 >= 5.3.3 sqlite3 php5-sqlite php5-mbstring php5-zip php5-json php5-posix curl php5-curl php5-gd php5-ctype php5-xmlreader php5-xmlwriter php5-zlib php5-pear php5-iconv
BuildRequires:  apache2 unzip
%else
# SLES 11 requires
# require mysql directly for SLES 11
Requires:       apache2 apache2-mod_php53 php53 >= 5.3.3 mysql php53-sqlite php53-mbstring php53-zip php53-json php53-posix curl php53-curl php53-gd php53-ctype php53-xmlreader php53-xmlwriter php53-zlib php53-pear php53-iconv
BuildRequires:  apache2 unzip
%endif
%endif

Requires:       curl %{name}-3rdparty
%if 0%{?suse_version}
# SUSE does not include the fileinfo module in php-common.
Requires:       php-fileinfo
%if 0%{?suse_version} != 1110
Recommends:     php5-mysql mysql php5-imagick libreoffice-writer
%else
Recommends:     php53-mysql mysql php53-imagick
%endif
%else
Requires:       mysql
%endif

%description
ownCloud Server provides you a private file sync and share
cloud. Host this server to easily sync business or private documents
across all your devices, and share those documents with other users of
your ownCloud server on their devices.

ownCloud - Your Cloud, Your Data, Your Way!  www.owncloud.org


%package 3rdparty
License:      PHP-3.01
Group:        Development/Libraries/PHP
Summary:      3rdparty libraries for ownCloud
Requires:     %{name} = %{version}
%description 3rdparty
3rdparty libraries needed for running ownCloud. 
Contained in separate package due to different source code licenses.


%prep
%setup -q -n owncloud
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
#%%patch0 -p0

%build

%install
# no server side java code contained, alarm is false
export NO_BRP_CHECK_BYTECODE_VERSION=true
idir=$RPM_BUILD_ROOT/%{apache_serverroot}/%{name}
mkdir -p $idir
mkdir -p $idir/data
cp -aRf * $idir
cp -aRf .htaccess $idir
# $idir/l10n to disappear in future
rm -f $idir/l10n/l10n.pl

if [ ! -f $idir/robots.txt ]; then
  install -p -D -m 644 %{SOURCE4} $idir/robots.txt
fi

# create the AllowOverride directive
install -p -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{apache_confdir}/owncloud.conf
ocpath="%{apache_serverroot}/%{name}"
sed -i -e"s|DATAPATH|${ocpath}|g" $RPM_BUILD_ROOT/%{apache_confdir}/owncloud.conf

# clean sources of odfviewer
rm -rf ${idir}/apps/files_odfviewer/src
rm -rf ${idir}/3rdparty/phpass/c
rm -rf ${idir}/3rdparty/phpdocx/pdf/lib/ttf2ufm
rm -rf ${idir}/3rdparty/phpdocx/pdf/tcpdf/fonts/utils/ttf2ufm
rm -rf ${idir}/3rdparty/phpdocx/pdf/tcpdf/fonts/utils/pfm2afm

# not needed for distro packages
rm -f ${idir}/indie.json

%if 0%{?suse_version}
# link duplicate doc files
%fdupes -s $RPM_BUILD_ROOT/%{apache_serverroot}/%{name}
%endif

# relabel data directory for SELinux to allow ownCloud write access on redhat platforms
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
if [ -x /usr/sbin/sestatus ] ; then \
  sestatus | grep -E '^(SELinux status|Current).*(enforcing|permissive)' > /dev/null && { 
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/%{name}/data'
    restorecon '/var/www/html/%{name}/data'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/%{name}/config'
    restorecon '/var/www/html/%{name}/config'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/%{name}/apps'
    restorecon '/var/www/html/%{name}/apps'
  }
fi
true
%endif


%postun
# remove SELinux ownCloud label if not updating
[ $1 -eq 0 ] || exit 0
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
if [ -x /usr/sbin/sestatus ] ; then \
  sestatus | grep -E '^(SELinux status|Current).*(enforcing|permissive)' > /dev/null && { 
    semanage fcontext -l | grep '/var/www/%{name}/data' && {
      semanage fcontext -d -t httpd_sys_rw_content_t '/var/www/html/%{name}/data'
      restorecon '/var/www/html/%{name}/data'
    }
    semanage fcontext -l | grep '/var/www/html/owncloud/config' && {
      semanage fcontext -d -t httpd_sys_rw_content_t '/var/www/html/%{name}/config'
      restorecon '/var/www/html/%{name}/config'
    }
    semanage fcontext -l | grep '/var/www/html/%{name}/apps' && {
      semanage fcontext -d -t httpd_sys_rw_content_t '/var/www/html/%{name}/apps'
      restorecon '/var/www/html/%{name}/apps'
    }
  }
fi
true
%endif

%pre
# avoid fatal php errors, while we are changing files
# https://github.com/owncloud/core/issues/10953
#
# We don't do this for new installs. Only for updates.
# If the first argument to pre is 1, the RPM operation is an initial installation. If the argument is 2, 
# the operation is an upgrade from an existing version to a new one.
if [ $1 -gt 1 -a ! -s /tmp/apache_stopped_during_owncloud_install ]; then	
  echo "%{name} update: Checking for running Apache"
  # FIXME: this above should make it idempotent -- a requirement with openSUSE.
  # it does not work.
%if 0%{?suse_version} && 0
%if 0%{?suse_version} <= 1110
  rcapache2 status       | grep running > /tmp/apache_stopped_during_owncloud_install
  rcapache2 stop
%else
  service apache2 status | grep running > /tmp/apache_stopped_during_owncloud_install
  service apache2 stop
%endif
%endif
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
  service httpd status | grep running > /tmp/apache_stopped_during_owncloud_install
  service httpd stop
%endif
fi
if [ -s /tmp/apache_stopped_during_owncloud_install ]; then
  echo "%{name} pre-install: Stopping Apache"
fi

if [ $1 -eq 1 ]; then
    echo "%{name}-server: First install starting"
else
    echo "%{name}-server: installing upgrade ..."
fi
# https://github.com/owncloud/core/issues/12125
# https://github.com/owncloud/pull/issues/19661
if [ -x %{ocphp_bin}/php -a -f %{oc_dir}/occ ]; then
  echo "%{name}: occ maintenance:mode --on"
  su %{oc_user} -s /bin/sh -c "cd %{oc_dir}; PATH=%{ocphp_bin}:$PATH php ./occ maintenance:mode --on" || true
  echo yes > %{statedir}/occ_maintenance_mode_during_owncloud_install
fi


%post
if [ $1 -eq 1 ]; then
    echo "%{name} First install complete"
else
    echo "%{name} Upgrade complete"
fi

# must ignore errors with e.g.  '|| true' or we die in openSUSEs horrible post build checks.
# https://github.com/owncloud/core/issues/12125 needed occ calls.
# https://github.com/owncloud/core/issues/17583 correct occ usage.
if [ -s %{statedir}/occ_maintenance_mode_during_owncloud_install ]; then
    # https://github.com/owncloud/core/pull/19508
    # https://github.com/owncloud/core/pull/19661
    echo  "Leaving server in maintenance mode. Please run occ upgrade manually."
    echo  ""
    echo  "See https://doc.owncloud.org/server/8.0/admin_manual/maintenance/upgrade.html"
    echo  ""
fi
rm -f %{statedir}/occ_maintenance_mode_during_owncloud_install


%if 0%{?suse_version}
# make sure php5 is not in APACHE_MODULES, so that we don't create dups.
perl -pani -e 's@^(APACHE_MODULES=".*)\bphp5\b@$1@' /etc/sysconfig/apache2
# add php5 to APACHE_MODULES
perl -pani -e 's@^(APACHE_MODULES=")@${1}php5 @' /etc/sysconfig/apache2
%endif

if [ -s /tmp/apache_stopped_during_owncloud_install ]; then
  echo "%{name} post-install: Restarting Apache"
  ## If we stopped apache in pre section, we now should restart. -- but *ONLY* then!
  ## Maybe delegate that task to occ upgrade? They also need to handle this, somehow.
%if 0%{?suse_version}
%if 0%{?suse_version} <= 1110
  rcapache2 start
%else
  service apache2 start
%endif
%endif
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
  service httpd start
%endif
fi
rm -f /tmp/apache_stopped_during_owncloud_install

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(0640,root,%{apache_group},0750)
%exclude %{apache_serverroot}/%{name}/3rdparty/PEAR*
%exclude %{apache_serverroot}/%{name}/3rdparty/System.php

%dir %{apache_serverroot}/%{name}
%{apache_serverroot}/%{name}/3rdparty
%doc %{apache_serverroot}/%{name}/AUTHORS
%doc %{apache_serverroot}/%{name}/COPYING-AGPL
%{apache_serverroot}/%{name}/core
%{apache_serverroot}/%{name}/db_structure.xml
%{apache_serverroot}/%{name}/index.php
## $idir/l10n to disappear in future
%{apache_serverroot}/%{name}/l10n
%{apache_serverroot}/%{name}/lib
%{apache_serverroot}/%{name}/ocs
%{apache_serverroot}/%{name}/public.php
%doc %{apache_serverroot}/%{name}/README*
%{apache_serverroot}/%{name}/remote.php
%{apache_serverroot}/%{name}/search
%{apache_serverroot}/%{name}/settings
%{apache_serverroot}/%{name}/status.php
%{apache_serverroot}/%{name}/themes
%{apache_serverroot}/%{name}/cron.php
%{apache_serverroot}/%{name}/.htaccess
%{apache_serverroot}/%{name}/robots.txt
%{apache_serverroot}/%{name}/index.html
%{apache_serverroot}/%{name}/console.php
%{apache_serverroot}/%{name}/version.php

%defattr(0755,root,%{apache_group},0750)
%{apache_serverroot}/%{name}/occ
%defattr(-,%{apache_user},%{apache_group},0770)
%{apache_serverroot}/%{name}/data
# config can be chown-ed to root:www after the initial DB config is done.
%dir %{apache_serverroot}/%{name}/config
%dir %{apache_serverroot}/%{name}/apps

%defattr(0640,root,%{apache_group},0750)
%{apache_serverroot}/%{name}/apps/*
%{apache_serverroot}/%{name}/config/*
%{apache_serverroot}/%{name}/config/.htaccess

%config %attr(0644,root,root) %{apache_confdir}/owncloud.conf

%doc README README.SELinux

%files 3rdparty
%defattr(0640,root,%{apache_group},0750)
%{apache_serverroot}/%{name}/3rdparty/PEAR/
%{apache_serverroot}/%{name}/3rdparty/PEAR.php
%{apache_serverroot}/%{name}/3rdparty/PEAR5.php
%{apache_serverroot}/%{name}/3rdparty/PEAR-LICENSE
%{apache_serverroot}/%{name}/3rdparty/System.php

%changelog
