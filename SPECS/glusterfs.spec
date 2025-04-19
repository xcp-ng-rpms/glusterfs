# XCP-ng: spec file synced from upstream glusterfs tarball and adapted

%global _hardened_build 1

%global _for_fedora_koji_builds 0

# uncomment and add '%' to use the prereltag for pre-releases
# %%global prereltag qa3

##-----------------------------------------------------------------------------
## All argument definitions should be placed here and keep them sorted
##

# asan
# if you wish to compile an rpm with address sanitizer...
# rpmbuild -ta glusterfs-11.1.tar.gz --with asan
%{?_with_asan:%global _with_asan --enable-asan}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%global _with_asan %{nil}
%endif

# cmocka
# if you wish to compile an rpm with cmocka unit testing...
# rpmbuild -ta glusterfs-11.1.tar.gz --with cmocka
%{?_with_cmocka:%global _with_cmocka --enable-cmocka}

# debug
# if you wish to compile an rpm with debugging...
# rpmbuild -ta glusterfs-11.1.tar.gz --with debug
%{?_with_debug:%global _with_debug --enable-debug}

# epoll
# if you wish to compile an rpm without epoll...
# rpmbuild -ta glusterfs-11.1.tar.gz --without epoll
%{?_without_epoll:%global _without_epoll --disable-epoll}

# fusermount
# if you wish to compile an rpm without fusermount...
# rpmbuild -ta glusterfs-11.1.tar.gz --without fusermount
%{?_without_fusermount:%global _without_fusermount --disable-fusermount}

# geo-rep
# if you wish to compile an rpm without geo-replication support, compile like this...
# rpmbuild -ta glusterfs-11.1.tar.gz --without georeplication
%{?_without_georeplication:%global _without_georeplication --disable-georeplication}

# gnfs
# if you wish to compile an rpm with the legacy gNFS server xlator
# rpmbuild -ta glusterfs-11.1.tar.gz --with gnfs
%{?_with_gnfs:%global _with_gnfs --enable-gnfs}

# ipv6default
# if you wish to compile an rpm with IPv6 default...
# rpmbuild -ta glusterfs-11.1.tar.gz --with ipv6default
%{?_with_ipv6default:%global _with_ipv6default --with-ipv6-default}

# linux-io_uring
# If you wish to compile an rpm without linux-io_uring support...
# rpmbuild -ta  glusterfs-11.1.tar.gz --without linux-io_uring
%{?_without_linux_io_uring:%global _without_linux_io_uring --disable-linux-io_uring}

# Disable linux-io_uring on unsupported distros.
%if ( 0%{?fedora} && 0%{?fedora} <= 32 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
%global _without_linux_io_uring --disable-linux-io_uring
%endif

# libtirpc
# if you wish to compile an rpm without TIRPC (i.e. use legacy glibc rpc)
# rpmbuild -ta glusterfs-11.1.tar.gz --without libtirpc
%{?_without_libtirpc:%global _without_libtirpc --without-libtirpc}

# libtcmalloc
# if you wish to compile an rpm without tcmalloc (i.e. use gluster mempool)
# rpmbuild -ta glusterfs-11.1.tar.gz --without tcmalloc
%{?_without_tcmalloc:%global _without_tcmalloc --without-tcmalloc}

%ifnarch x86_64
%global _without_tcmalloc --without-tcmalloc
%endif

# Do not use libtirpc on EL6, it does not have xdr_uint64_t() and xdr_uint32_t
# Do not use libtirpc on EL7, it does not have xdr_sizeof()
%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
%global _without_libtirpc --without-libtirpc
%endif


# ocf
# if you wish to compile an rpm without the OCF resource agents...
# rpmbuild -ta glusterfs-11.1.tar.gz --without ocf
%{?_without_ocf:%global _without_ocf --without-ocf}

# server
# if you wish to build rpms without server components, compile like this
# rpmbuild -ta glusterfs-11.1.tar.gz --without server
%{?_without_server:%global _without_server --without-server}

# disable server components forcefully as rhel <= 6
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
%global _without_server --without-server
%endif

# syslog
# if you wish to build rpms without syslog logging, compile like this
# rpmbuild -ta glusterfs-11.1.tar.gz --without syslog
%{?_without_syslog:%global _without_syslog --disable-syslog}

# disable syslog forcefully as rhel <= 6 doesn't have rsyslog or rsyslog-mmcount
# Fedora deprecated syslog, see
#  https://fedoraproject.org/wiki/Changes/NoDefaultSyslog
# (And what about RHEL7?)
%if ( 0%{?fedora} && 0%{?fedora} >= 20 ) || ( 0%{?rhel} && 0%{?rhel} <= 6 )
%global _without_syslog --disable-syslog
%endif

# tsan
# if you wish to compile an rpm with thread sanitizer...
# rpmbuild -ta glusterfs-11.1.tar.gz --with tsan
%{?_with_tsan:%global _with_tsan --enable-tsan}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%global _with_tsan %{nil}
%endif

# valgrind
# if you wish to compile an rpm to run all processes under valgrind...
# rpmbuild -ta glusterfs-11.1.tar.gz --with valgrind
%{?_with_valgrind:%global _with_valgrind --enable-valgrind}

##-----------------------------------------------------------------------------
## All %%global definitions should be placed here and keep them sorted
##

# selinux booleans whose defalut value needs modification
# these booleans will be consumed by "%%selinux_set_booleans" macro.
%if ( 0%{?rhel} && 0%{?rhel} >= 8 )
%global selinuxbooleans rsync_full_access=1 rsync_client=1
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
%global _with_systemd true
%endif

# XCP-ng: no firewalld on XCP-ng
# %%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 7 )
# %%global _with_firewalld --enable-firewalld
# %%endif

%if 0%{?_tmpfilesdir:1}
%global _with_tmpfilesdir --with-tmpfilesdir=%{_tmpfilesdir}
%else
%global _with_tmpfilesdir --without-tmpfilesdir
%endif

# without server should also disable some server-only components
%if 0%{?_without_server:1}
%global _without_events --disable-events
%global _without_georeplication --disable-georeplication
%global _without_linux_io_uring --disable-linux-io_uring
%global _with_gnfs %{nil}
%global _without_ocf --without-ocf
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 7 || 0%{?xenserver} >= 8)
%global _usepython3 1
%global _pythonver 3
%else
%global _usepython3 0
%global _pythonver 2
%endif

# From https://fedoraproject.org/wiki/Packaging:Python#Macros
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(python2 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global _rundir %{_localstatedir}/run
%endif

%if ( 0%{?_with_systemd:1} )
%global service_start()   /bin/systemctl --quiet start %1.service || : \
%{nil}
%global service_stop()    /bin/systemctl --quiet stop %1.service || :\
%{nil}
%global service_install() install -D -p -m 0644 %1.service %{buildroot}%2 \
%{nil}
# can't seem to make a generic macro that works
%global glusterd_svcfile   %{_unitdir}/glusterd.service
%global glusterfsd_svcfile %{_unitdir}/glusterfsd.service
%global glusterta_svcfile %{_unitdir}/gluster-ta-volume.service
%global glustereventsd_svcfile %{_unitdir}/glustereventsd.service
%global glusterfssharedstorage_svcfile %{_unitdir}/glusterfssharedstorage.service
%else
%global systemd_post()  /sbin/chkconfig --add %1 >/dev/null 2>&1 || : \
%{nil}
%global systemd_preun() /sbin/chkconfig --del %1 >/dev/null 2>&1 || : \
%{nil}
%global systemd_postun_with_restart() /sbin/service %1 condrestart >/dev/null 2>&1 || : \
%{nil}
%global service_start()   /sbin/service %1 start >/dev/null 2>&1 || : \
%{nil}
%global service_stop()    /sbin/service %1 stop >/dev/null 2>&1 || : \
%{nil}
%global service_install() install -D -p -m 0755 %1.init %{buildroot}%2 \
%{nil}
# can't seem to make a generic macro that works
%global glusterd_svcfile   %{_sysconfdir}/init.d/glusterd
%global glusterfsd_svcfile %{_sysconfdir}/init.d/glusterfsd
%global glustereventsd_svcfile %{_sysconfdir}/init.d/glustereventsd
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# We do not want to generate useless provides and requires for xlator
# .so files to be set for glusterfs packages.
# Filter all generated:
#
# TODO: RHEL5 does not have a convenient solution
%if ( 0%{?rhel} == 6 )
# filter_setup exists in RHEL6 only
%filter_provides_in %{_libdir}/glusterfs/%{version}/
%global __filter_from_req %{?__filter_from_req} | grep -v -P '^(?!lib).*\.so.*$'
%filter_setup
%else
# modern rpm and current Fedora do not generate requires when the
# provides are filtered
%global __provides_exclude_from ^%{_libdir}/glusterfs/%{version}/.*$
%endif

%global bashcompdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%if "%{bashcompdir}" == ""
%global bashcompdir ${sysconfdir}/bash_completion.d
%endif

##-----------------------------------------------------------------------------
## All package definitions should be placed here in alphabetical order
##
Summary:          Distributed File System
%if ( 0%{_for_fedora_koji_builds} )
Name:             glusterfs
Version:          3.8.0
Release:          0.1%{?prereltag:.%{prereltag}}%{?dist}
%else
Name:             glusterfs
Version:          11.1
Release:          1%{?dist}
%endif
License:          GPLv2 or LGPLv3+
URL:              http://docs.gluster.org/
%if ( 0%{_for_fedora_koji_builds} )
Source0:          http://bits.gluster.org/pub/gluster/glusterfs/src/glusterfs-%{version}%{?prereltag}.tar.gz
Source1:          glusterd.sysconfig
Source2:          glusterfsd.sysconfig
Source7:          glusterfsd.service
Source8:          glusterfsd.init
%else
Source0:          glusterfs-11.1.tar.gz
%endif

BuildRoot:        %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(pre):    shadow-utils
%if ( 0%{?_with_systemd:1} )
BuildRequires:    systemd
%endif

%if ( 0%{!?_without_tcmalloc:1} )
Requires:         gperftools-libs%{?_isa}
%endif

Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Requires:         libgfrpc0%{?_isa} = %{version}-%{release}
Requires:         libgfxdr0%{?_isa} = %{version}-%{release}
%if ( 0%{?_with_systemd:1} )
%{?systemd_requires}
%endif
%if 0%{?_with_asan:1} && !( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:    libasan
%endif
%if 0%{?_with_tsan:1} && !( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:    libtsan
%endif
BuildRequires:    bison flex
BuildRequires:    gcc make libtool
BuildRequires:    ncurses-devel readline-devel
BuildRequires:    libxml2-devel openssl-devel openssl
BuildRequires:    libaio-devel libacl-devel
BuildRequires:    python%{_pythonver}-devel
%if ( 0%{!?_without_tcmalloc:1} )
BuildRequires:    gperftools-devel
%endif
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
BuildRequires:    python-ctypes
%endif
%if ( 0%{?_with_ipv6default:1} ) || ( 0%{!?_without_libtirpc:1} )
BuildRequires:    libtirpc-devel
%endif
%if ( 0%{?fedora} && 0%{?fedora} > 27 ) || ( 0%{?rhel} && 0%{?rhel} > 7 )
BuildRequires:    rpcgen
%endif
BuildRequires:    userspace-rcu-devel >= 0.7
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
BuildRequires:    automake
%endif
BuildRequires:    libuuid-devel
%if ( 0%{?_with_cmocka:1} )
BuildRequires:    libcmocka-devel >= 1.0.1
%endif
%if ( 0%{!?_without_georeplication:1} )
BuildRequires:    libattr-devel
%endif

%if (0%{?_with_firewalld:1})
BuildRequires:    firewalld
%endif

%if ( 0%{!?_without_linux_io_uring:1} )
BuildRequires:    liburing-devel
%endif

Obsoletes:        %{name}-common < %{version}-%{release}
Obsoletes:        %{name}-core < %{version}-%{release}
Obsoletes:        %{name}-rdma < %{version}-%{release}
%if ( 0%{!?_with_gnfs:1} )
Obsoletes:        %{name}-gnfs < %{version}-%{release}
%endif
Provides:         %{name}-common = %{version}-%{release}
Provides:         %{name}-core = %{version}-%{release}

%description
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package includes the glusterfs binary, the glusterfsd daemon and the
libglusterfs and glusterfs translator modules common to both GlusterFS server
and client framework.

%package cli
Summary:          GlusterFS CLI
%if ( ! (0%{?rhel} && 0%{?rhel} < 7) )
BuildRequires:    pkgconfig(bash-completion)
# bash-completion >= 1.90 satisfies this requirement.
# If it is not available, the condition can be adapted
# and the completion script will be installed in the backwards compatible
# %{sysconfdir}/bash_completion.d
%endif
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}

%description cli
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the GlusterFS CLI application and its man page

%package cloudsync-plugins
Summary:          Cloudsync Plugins
BuildRequires:    libcurl-devel

%description cloudsync-plugins
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides cloudsync plugins for archival feature.

%package extra-xlators
Summary:          Extra Gluster filesystem Translators
# We need python-gluster rpm for gluster module's __init__.py in Python
# site-packages area
Requires:         python%{_pythonver}-gluster = %{version}-%{release}
Requires:         python%{_pythonver}

%description extra-xlators
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides extra filesystem Translators, such as Glupy,
for GlusterFS.

%package fuse
Summary:          Fuse client
BuildRequires:    fuse-devel
Requires:         attr
Requires:         psmisc

Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-client-xlators%{?_isa} = %{version}-%{release}

Obsoletes:        %{name}-client < %{version}-%{release}
Provides:         %{name}-client = %{version}-%{release}

%description fuse
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides support to FUSE based clients and inlcudes the
glusterfs(d) binary.

%if ( 0%{!?_without_server:1} )
%package ganesha
Summary:          NFS-Ganesha configuration
Group:            Applications/File

Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         nfs-ganesha-selinux >= 2.7.6
Requires:         nfs-ganesha-gluster >= 2.7.6
Requires:         pcs >= 0.10.0
Requires:         resource-agents >= 4.2.0
Requires:         dbus

%if ( 0%{?rhel} && 0%{?rhel} == 6 )
Requires:         cman, pacemaker, corosync
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 5 )
# we need portblock resource-agent in 3.9.5 and later.
Requires:         net-tools
%endif

%if ( 0%{?fedora} && 0%{?fedora} > 25  || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
Requires: selinux-policy >= 3.13.1-160
Requires(post):   policycoreutils-python
Requires(postun): policycoreutils-python
%else
Requires(post):   policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils
%endif
%endif

%description ganesha
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the configuration and related files for using
NFS-Ganesha as the NFS server using GlusterFS
%endif

%if ( 0%{!?_without_georeplication:1} )
%package geo-replication
Summary:          GlusterFS Geo-replication
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         python%{_pythonver}
Requires:         python%{_pythonver}-prettytable
Requires:         python%{_pythonver}-gluster = %{version}-%{release}

Requires:         rsync
Requires:         util-linux
Requires:         tar

# required for setting selinux bools
%if ( 0%{?rhel} && 0%{?rhel} >= 8 )
Requires(post):      policycoreutils-python-utils
Requires(postun):    policycoreutils-python-utils
Requires:            selinux-policy-targeted
Requires(post):      selinux-policy-targeted
BuildRequires:       selinux-policy-devel
%endif

%description geo-replication
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides support to geo-replication.
%endif

%if ( 0%{?_with_gnfs:1} )
%package gnfs
Summary:          GlusterFS gNFS server
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-client-xlators%{?_isa} = %{version}-%{release}
Requires:         nfs-utils

%description gnfs
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the glusterfs legacy gNFS server xlator
%endif

%package -n libglusterfs0
Summary:          GlusterFS libglusterfs library
Requires:         libgfrpc0%{?_isa} = %{version}-%{release}
Requires:         libgfxdr0%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-libs <= %{version}-%{release}
Provides:         %{name}-libs = %{version}-%{release}

%description -n libglusterfs0
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the base libglusterfs library

%package -n libglusterfs-devel
Summary:          GlusterFS libglusterfs library
Requires:         libgfrpc-devel%{?_isa} = %{version}-%{release}
Requires:         libgfxdr-devel%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-devel <= %{version}-%{release}
Provides:         %{name}-devel = %{version}-%{release}

%description -n libglusterfs-devel
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides libglusterfs.so and the gluster C header files.

%package -n libgfapi0
Summary:          GlusterFS api library
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Requires:         %{name}-client-xlators%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-api <= %{version}-%{release}
Provides:         %{name}-api = %{version}-%{release}

%description -n libgfapi0
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the glusterfs libgfapi library.

%package -n libgfapi-devel
Summary:          Development Libraries
Requires:         libglusterfs-devel%{?_isa} = %{version}-%{release}
Requires:         libacl-devel
Obsoletes:        %{name}-api-devel <= %{version}-%{release}
Provides:         %{name}-api-devel = %{version}-%{release}

%description -n libgfapi-devel
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides libgfapi.so and the api C header files.

%package -n libgfchangelog0
Summary:          GlusterFS libchangelog library
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-libs <= %{version}-%{release}

%description -n libgfchangelog0
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the libgfchangelog library

%package -n libgfchangelog-devel
Summary:          GlusterFS libchangelog library
Requires:         libglusterfs-devel%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-devel <= %{version}-%{release}

%description -n libgfchangelog-devel
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides libgfchangelog.so and changelog C header files.

%package -n libgfrpc0
Summary:          GlusterFS libgfrpc0 library
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-libs <= %{version}-%{release}

%description -n libgfrpc0
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the libgfrpc library

%package -n libgfrpc-devel
Summary:          GlusterFS libgfrpc library
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-devel <= %{version}-%{release}

%description -n libgfrpc-devel
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides libgfrpc.so and rpc C header files.

%package -n libgfxdr0
Summary:          GlusterFS libgfxdr0 library
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-libs <= %{version}-%{release}

%description -n libgfxdr0
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the libgfxdr library

%package -n libgfxdr-devel
Summary:          GlusterFS libgfxdr library
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Obsoletes:        %{name}-devel <= %{version}-%{release}

%description -n libgfxdr-devel
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides libgfxdr.so.

%package -n python%{_pythonver}-gluster
Summary:          GlusterFS python library
Requires:         python%{_pythonver}
%if ( ! %{_usepython3} )
%{?python_provide:%python_provide python-gluster}
Provides:         python-gluster = %{version}-%{release}
Obsoletes:        python-gluster < 3.10
%endif

%description -n python%{_pythonver}-gluster
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package contains the python modules of GlusterFS and own gluster
namespace.

%package regression-tests
Summary:          Development Tools
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-fuse%{?_isa} = %{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
## thin provisioning support
Requires:         lvm2 >= 2.02.89
Requires:         perl(App::Prove) perl(Test::Harness) gcc util-linux-ng
Requires:         python%{_pythonver}
Requires:         attr dbench file git libacl-devel net-tools
Requires:         nfs-utils xfsprogs yajl psmisc bc

%description regression-tests
The Gluster Test Framework, is a suite of scripts used for
regression testing of Gluster.

%if ( 0%{!?_without_ocf:1} )
%package resource-agents
Summary:          OCF Resource Agents for GlusterFS
License:          GPLv3+
BuildArch:        noarch
# this Group handling comes from the Fedora resource-agents package
# for glusterd
Requires:         %{name}-server = %{version}-%{release}
# depending on the distribution, we need pacemaker or resource-agents
Requires:         %{_prefix}/lib/ocf/resource.d

%description resource-agents
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the resource agents which plug glusterd into
Open Cluster Framework (OCF) compliant cluster resource managers,
like Pacemaker.
%endif

%if ( 0%{!?_without_server:1} )
%package server
Summary:          Clustered file-system server
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-cli%{?_isa} = %{version}-%{release}
Requires:         libglusterfs0%{?_isa} = %{version}-%{release}
Requires:         libgfchangelog0%{?_isa} = %{version}-%{release}
%if ( 0%{?fedora} && 0%{?fedora} >= 30  || ( 0%{?rhel} && 0%{?rhel} >= 8 ) )
Requires:         glusterfs-selinux >= 0.1.0-2
%endif
# some daemons (like quota) use a fuse-mount, glusterfsd is part of -fuse
Requires:         %{name}-fuse%{?_isa} = %{version}-%{release}
# self-heal daemon, rebalance, nfs-server etc. are actually clients
Requires:         libgfapi0%{?_isa} = %{version}-%{release}
Requires:         %{name}-client-xlators%{?_isa} = %{version}-%{release}
# lvm2 for snapshot, and nfs-utils and rpcbind/portmap for gnfs server
Requires:         lvm2
%if ( 0%{?_with_systemd:1} )
%{?systemd_requires}
%else
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/service
Requires(preun):  /sbin/chkconfig
Requires(postun): /sbin/service
%endif
%if (0%{?_with_firewalld:1})
# we install firewalld rules, so we need to have the directory owned
%if ( 0%{!?rhel} )
# not on RHEL because firewalld-filesystem appeared in 7.3
# when EL7 rpm gets weak dependencies we can add a Suggests:
Requires:         firewalld-filesystem
%endif
%endif
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
Requires:         rpcbind
%else
Requires:         portmap
%endif
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
Requires:         python-argparse
%endif
%if ( 0%{?fedora} && 0%{?fedora} > 27 ) || ( 0%{?rhel} && 0%{?rhel} > 7 )
Requires:         python%{_pythonver}-pyxattr
%else
Requires:         pyxattr
%endif
%if (0%{?_with_valgrind:1})
Requires:         valgrind
%endif

%description server
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the glusterfs server daemon.
%endif

%package thin-arbiter
Summary:          GlusterFS thin-arbiter module
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{version}-%{release}

%description thin-arbiter
This package provides a tie-breaker functionality to GlusterFS
replicate volume. It includes translators required to provide the
functionality, and also few other scripts required for getting the setup done.

This package provides the glusterfs thin-arbiter translator.

%package client-xlators
Summary:          GlusterFS client-side translators

%description client-xlators
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over TCP/IP interconnect
into one large parallel network filesystem. GlusterFS is one of the
most sophisticated file systems in terms of features and extensibility.
It borrows a powerful concept called Translators from GNU Hurd kernel.
Much of the code in GlusterFS is in user space and easily manageable.

This package provides the translators needed on any GlusterFS client.

%if ( 0%{!?_without_events:1} )
%package events
Summary:          GlusterFS Events
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         python%{_pythonver} python%{_pythonver}-prettytable
Requires:         python%{_pythonver}-gluster = %{version}-%{release}
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
Requires:         python-requests
%else
Requires:         python%{_pythonver}-requests
%endif
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
Requires:         python-argparse
%endif
%if ( 0%{?_with_systemd:1} )
%{?systemd_requires}
%endif

%description events
GlusterFS Events

%endif

%prep
%setup -q -n %{name}-%{version}%{?prereltag}
%if ( ! %{_usepython3} )
echo "fixing python shebangs..."
for f in api events extras geo-replication libglusterfs tools xlators; do
find $f -type f -exec sed -i 's|/usr/bin/python3|/usr/bin/python2|' {} \;
done
%endif

%build

# RHEL6 and earlier need to manually replace config.guess and config.sub
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
./autogen.sh
%endif

%configure \
        %{?_with_asan} \
        %{?_with_cmocka} \
        %{?_with_debug} \
        %{?_with_firewalld} \
        %{?_with_gnfs} \
        %{?_with_tmpfilesdir} \
        %{?_with_tsan} \
        %{?_with_valgrind} \
        %{?_without_epoll} \
        %{?_without_events} \
        %{?_without_fusermount} \
        %{?_without_georeplication} \
        %{?_without_ocf} \
        %{?_without_server} \
        %{?_without_syslog} \
        %{?_with_ipv6default} \
        %{?_without_linux_io_uring} \
        %{?_without_libtirpc} \
        %{?_without_tcmalloc}

# fix hardening and remove rpath in shlibs
%if ( 0%{?fedora} && 0%{?fedora} > 17 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
sed -i 's| \\\$compiler_flags |&\\\$LDFLAGS |' libtool
%endif
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|' libtool

make %{?_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%if ( 0%{!?_without_server:1} )
%if ( 0%{_for_fedora_koji_builds} )
install -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterd
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd
%else
install -D -p -m 0644 extras/glusterd-sysconfig \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterd
%endif
%endif

mkdir -p %{buildroot}%{_localstatedir}/log/glusterd
mkdir -p %{buildroot}%{_localstatedir}/log/glusterfs
mkdir -p %{buildroot}%{_localstatedir}/log/glusterfsd
mkdir -p %{buildroot}%{_rundir}/gluster

# Remove unwanted files from all the shared libraries
find %{buildroot}%{_libdir} -name '*.a' -delete
find %{buildroot}%{_libdir} -name '*.la' -delete

# Remove installed docs, the ones we want are included by %%doc, in
# /usr/share/doc/glusterfs or /usr/share/doc/glusterfs-x.y.z depending
# on the distribution
%if ( 0%{?fedora} && 0%{?fedora} > 19 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
rm -rf %{buildroot}%{_pkgdocdir}/*
%else
rm -rf %{buildroot}%{_defaultdocdir}/%{name}
mkdir -p %{buildroot}%{_pkgdocdir}
%endif
head -50 ChangeLog > ChangeLog.head && mv ChangeLog.head ChangeLog
cat << EOM >> ChangeLog

More commit messages for this ChangeLog can be found at
https://forge.gluster.org/glusterfs-core/glusterfs/commits/v%{version}%{?prereltag}
EOM

# Remove benchmarking and other unpackaged files
# make install always puts these in %%{_defaultdocdir}/%%{name} so don't
# use %%{_pkgdocdir}; that will be wrong on later Fedora distributions
rm -rf %{buildroot}%{_defaultdocdir}/%{name}/benchmarking
rm -f %{buildroot}%{_defaultdocdir}/%{name}/glusterfs-mode.el
rm -f %{buildroot}%{_defaultdocdir}/%{name}/glusterfs.vim

%if ( 0%{!?_without_server:1} )
# Create working directory
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd

# Update configuration file to /var/lib working directory
sed -i 's|option working-directory /etc/glusterd|option working-directory %{_sharedstatedir}/glusterd|g' \
    %{buildroot}%{_sysconfdir}/glusterfs/glusterd.vol
%endif

# Install glusterfsd .service or init.d file
%if ( 0%{!?_without_server:1} )
%if ( 0%{_for_fedora_koji_builds} )
%service_install glusterfsd %{glusterfsd_svcfile}
%endif
%endif

install -D -p -m 0644 extras/glusterfs-logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs

# ganesha ghosts
%if ( 0%{!?_without_server:1} )
mkdir -p %{buildroot}%{_sysconfdir}/ganesha
touch %{buildroot}%{_sysconfdir}/ganesha/ganesha-ha.conf
mkdir -p %{buildroot}%{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/
touch %{buildroot}%{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha.conf
touch %{buildroot}%{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha-ha.conf
%endif

%if ( 0%{!?_without_georeplication:1} )
# geo-rep ghosts
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/geo-replication
touch %{buildroot}%{_sharedstatedir}/glusterd/geo-replication/gsyncd_template.conf
install -D -p -m 0644 extras/glusterfs-georep-logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-georep
%endif

%if ( 0%{!?_without_server:1} )
# the rest of the ghosts
touch %{buildroot}%{_sharedstatedir}/glusterd/glusterd.info
touch %{buildroot}%{_sharedstatedir}/glusterd/options
subdirs=(add-brick create copy-file delete gsync-create remove-brick reset set start stop)
for dir in ${subdirs[@]}; do
    mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/"$dir"/{pre,post}
done
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/glustershd
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/peers
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/vols
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/nfs/run
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/bitd
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/quotad
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/scrub
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/snaps
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/ss_brick
touch %{buildroot}%{_sharedstatedir}/glusterd/nfs/nfs-server.vol
touch %{buildroot}%{_sharedstatedir}/glusterd/nfs/run/nfs.pid
%endif

find ./tests ./run-tests.sh -type f | cpio -pd %{buildroot}%{_prefix}/share/glusterfs

%clean
rm -rf %{buildroot}

##-----------------------------------------------------------------------------
## All %%post should be placed here and keep them sorted
##
%post
/sbin/ldconfig
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%systemd_postun_with_restart rsyslog
%endif
%endif
exit 0

%if ( 0%{!?_without_events:1} )
%post events
%systemd_post glustereventsd
%endif

%if ( 0%{!?_without_server:1} )
%if ( 0%{?fedora} && 0%{?fedora} > 25 || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%post ganesha
# first install
if [ $1 -eq 1 ]; then
  %selinux_set_booleans ganesha_use_fusefs=1
fi
exit 0
%endif
%endif

%if ( 0%{!?_without_georeplication:1} )
%post geo-replication
%if ( 0%{?rhel} && 0%{?rhel} >= 8 )
if [ $1 -eq 1 ]; then
  %selinux_set_booleans %{selinuxbooleans}
fi
%endif
if [ $1 -ge 1 ]; then
    %systemd_postun_with_restart glusterd
fi
exit 0
%endif

%post -n libglusterfs0
/sbin/ldconfig

%post -n libgfapi0
/sbin/ldconfig

%post -n libgfchangelog0
/sbin/ldconfig

%post -n libgfrpc0
/sbin/ldconfig

%post -n libgfxdr0
/sbin/ldconfig

%if ( 0%{!?_without_server:1} )
%post server
# Legacy server
%systemd_post glusterd
%if ( 0%{_for_fedora_koji_builds} )
%systemd_post glusterfsd
%endif
# ".cmd_log_history" is renamed to "cmd_history.log" in GlusterFS-3.7 .
# While upgrading glusterfs-server package form GlusterFS version <= 3.6 to
# GlusterFS version 3.7, ".cmd_log_history" should be renamed to
# "cmd_history.log" to retain cli command history contents.
if [ -f %{_localstatedir}/log/glusterfs/.cmd_log_history ]; then
    mv %{_localstatedir}/log/glusterfs/.cmd_log_history \
       %{_localstatedir}/log/glusterfs/cmd_history.log
fi

# Genuine Fedora (and EPEL) builds never put gluster files in /etc; if
# there are any files in /etc from a prior gluster.org install, move them
# to /var/lib. (N.B. Starting with 3.3.0 all gluster files are in /var/lib
# in gluster.org RPMs.) Be careful to copy them on the off chance that
# /etc and /var/lib are on separate file systems
if [ -d /etc/glusterd -a ! -h %{_sharedstatedir}/glusterd ]; then
    mkdir -p %{_sharedstatedir}/glusterd
    cp -a /etc/glusterd %{_sharedstatedir}/glusterd
    rm -rf /etc/glusterd
    ln -sf %{_sharedstatedir}/glusterd /etc/glusterd
fi

# Rename old volfiles in an RPM-standard way.  These aren't actually
# considered package config files, so %%config doesn't work for them.
if [ -d %{_sharedstatedir}/glusterd/vols ]; then
    for file in $(find %{_sharedstatedir}/glusterd/vols -name '*.vol'); do
        newfile=${file}.rpmsave
        echo "warning: ${file} saved as ${newfile}"
        cp ${file} ${newfile}
    done
fi

# add marker translator
# but first make certain that there are no old libs around to bite us
# BZ 834847
if [ -e /etc/ld.so.conf.d/glusterfs.conf ]; then
    rm -f /etc/ld.so.conf.d/glusterfs.conf
    /sbin/ldconfig
fi

%if (0%{?_with_firewalld:1})
    %firewalld_reload
%endif

pidof -c -o %PPID -x glusterd &> /dev/null
if [ $? -eq 0 ]; then
    kill -9 `pgrep -f gsyncd.py` &> /dev/null

    killall --wait glusterd &> /dev/null
    glusterd --xlator-option *.upgrade=on -N

    #Cleaning leftover glusterd socket file which is created by glusterd in
    #rpm_script_t context.
    rm -f %{_rundir}/glusterd.socket

    # glusterd _was_ running, we killed it, it exited after *.upgrade=on,
    # so start it again
    %service_start glusterd
else
    glusterd --xlator-option *.upgrade=on -N

    #Cleaning leftover glusterd socket file which is created by glusterd in
    #rpm_script_t context.
    rm -f %{_rundir}/glusterd.socket
fi
exit 0
%endif

##-----------------------------------------------------------------------------
## All %%pre should be placed here and keep them sorted
##
%pre
getent group gluster > /dev/null || groupadd -r gluster
getent passwd gluster > /dev/null || useradd -r -g gluster -d %{_rundir}/gluster -s /sbin/nologin -c "GlusterFS daemons" gluster
exit 0

##-----------------------------------------------------------------------------
## All %%preun should be placed here and keep them sorted
##
%if ( 0%{!?_without_events:1} )
%preun events
if [ $1 -eq 0 ]; then
    if [ -f %glustereventsd_svcfile ]; then
        %service_stop glustereventsd
        %systemd_preun glustereventsd
    fi
fi
exit 0
%endif

%if ( 0%{!?_without_server:1} )
%preun server
if [ $1 -eq 0 ]; then
    if [ -f %glusterfsd_svcfile ]; then
        %service_stop glusterfsd
    fi
    %service_stop glusterd
    if [ -f %glusterfsd_svcfile ]; then
        %systemd_preun glusterfsd
    fi
    %systemd_preun glusterd
fi
if [ $1 -ge 1 ]; then
    if [ -f %glusterfsd_svcfile ]; then
        %systemd_postun_with_restart glusterfsd
    fi
    %systemd_postun_with_restart glusterd
fi
exit 0
%endif

%preun thin-arbiter
if [ $1 -eq 0 ]; then
    if [ -f %glusterta_svcfile ]; then
        %service_stop gluster-ta-volume
        %systemd_preun gluster-ta-volume
    fi
fi

##-----------------------------------------------------------------------------
## All %%postun should be placed here and keep them sorted
##
%postun
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%systemd_postun_with_restart rsyslog
%endif
%endif

%if ( 0%{!?_without_server:1} )
%postun server
%if (0%{?_with_firewalld:1})
    %firewalld_reload
%endif
exit 0
%endif

%if ( 0%{!?_without_server:1} )
%if ( 0%{?fedora} && 0%{?fedora} > 25  || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%postun ganesha
if [ $1 -eq 0 ]; then
  # use the value of ganesha_use_fusefs from before glusterfs-ganesha was installed
  %selinux_unset_booleans ganesha_use_fusefs=1
fi
exit 0
%endif
%endif

%if ( 0%{!?_without_georeplication:1} )
%postun geo-replication
%if ( 0%{?rhel} && 0%{?rhel} >= 8 )
if [ $1 -eq 0 ]; then
  %selinux_unset_booleans %{selinuxbooleans}
fi
exit 0
%endif
%endif

##-----------------------------------------------------------------------------
## All %%trigger should be placed here and keep them sorted
##
%if ( 0%{!?_without_server:1} )
%if ( 0%{?fedora} && 0%{?fedora} > 25  || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
# ensure ganesha_use_fusefs is on in case of policy mode switch (eg. mls->targeted)
%triggerin ganesha -- selinux-policy-targeted
semanage boolean -m ganesha_use_fusefs --on -S targeted
exit 0
%endif
%endif

##-----------------------------------------------------------------------------
## All %%files should be placed here and keep them grouped
##
%files
%doc ChangeLog COPYING-GPLV2 COPYING-LGPLV3 INSTALL README.md THANKS COMMITMENT
%{_mandir}/man8/*gluster*.8*
%if ( 0%{!?_without_server:1} )
%exclude %{_mandir}/man8/gluster.8*
%endif
%dir %{_localstatedir}/log/glusterfs
%if 0%{?!_without_server:1}
%dir %{_datadir}/glusterfs
%dir %{_datadir}/glusterfs/scripts
     %{_datadir}/glusterfs/scripts/post-upgrade-script-for-quota.sh
     %{_datadir}/glusterfs/scripts/pre-upgrade-script-for-quota.sh
%endif
# xlators that are needed on the client- and on the server-side
%dir %{_libdir}/glusterfs
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/auth
     %{_libdir}/glusterfs/%{version}%{?prereltag}/auth/addr.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/auth/login.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport
     %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport/socket.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/error-gen.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/delay-gen.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/io-stats.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/sink.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/trace.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/access-control.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/barrier.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/cdc.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/changelog.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/utime.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/gfid-access.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/namespace.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/read-only.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/shard.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/snapview-client.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/worm.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/cloudsync.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/meta.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/io-cache.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/io-threads.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/md-cache.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/open-behind.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/quick-read.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/read-ahead.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/readdir-ahead.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/stat-prefetch.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/write-behind.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/nl-cache.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/system
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/system/posix-acl.so
%dir %attr(0775,gluster,gluster) %{_rundir}/gluster
%if 0%{?_tmpfilesdir:1}
%{_tmpfilesdir}/gluster.conf
%endif

%if ( 0%{?_without_server:1} )
#exclude ganesha related files
%exclude %{_sysconfdir}/ganesha/ganesha-ha.conf.sample
%exclude %{_libexecdir}/ganesha/*
%exclude %{_prefix}/lib/ocf/resource.d/heartbeat/*
%endif

%files cli
%{_sbindir}/gluster
%{_mandir}/man8/gluster.8*
%{bashcompdir}/gluster.bash

%files cloudsync-plugins
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/cloudsync-plugins
     %{_libdir}/glusterfs/%{version}%{?prereltag}/cloudsync-plugins/cloudsyncs3.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/cloudsync-plugins/cloudsynccvlt.so

%files -n libglusterfs-devel
%dir %{_includedir}/glusterfs
     %{_includedir}/glusterfs/*.h
     %{_includedir}/glusterfs/server/*.h
%{_libdir}/libglusterfs.so

%files -n libgfapi-devel
%dir %{_includedir}/glusterfs/api
     %{_includedir}/glusterfs/api/*.h
%{_libdir}/libgfapi.so
%{_libdir}/pkgconfig/glusterfs-api.pc


%files -n libgfchangelog-devel
%dir %{_includedir}/glusterfs/gfchangelog
     %{_includedir}/glusterfs/gfchangelog/*.h
%{_libdir}/libgfchangelog.so
%{_libdir}/pkgconfig/libgfchangelog.pc

%files -n libgfrpc-devel
%dir %{_includedir}/glusterfs/rpc
     %{_includedir}/glusterfs/rpc/*.h
%{_libdir}/libgfrpc.so

%files -n libgfxdr-devel
%{_libdir}/libgfxdr.so

%files client-xlators
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/cluster
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/cluster/*.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol/client.so

%files extra-xlators
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/quiesce.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/playground
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/playground/template.so

%files fuse
# glusterfs is a symlink to glusterfsd, -server depends on -fuse.
%{_sbindir}/glusterfs
%{_sbindir}/glusterfsd
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfs
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/fuse.so
/sbin/mount.glusterfs
%if ( 0%{!?_without_fusermount:1} )
%{_bindir}/fusermount-glusterfs
%endif

%if ( 0%{?_with_gnfs:1} && 0%{!?_without_server:1} )
%files gnfs
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/nfs
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/nfs/server.so
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/nfs
%ghost      %attr(0600,-,-) %{_sharedstatedir}/glusterd/nfs/nfs-server.vol
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/nfs/run
%ghost      %attr(0600,-,-) %{_sharedstatedir}/glusterd/nfs/run/nfs.pid
%endif

%files thin-arbiter
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/thin-arbiter.so
%dir %{_datadir}/glusterfs/scripts
     %{_datadir}/glusterfs/scripts/setup-thin-arbiter.sh
%config %{_sysconfdir}/glusterfs/thin-arbiter.vol

%if ( 0%{?_with_systemd:1} )
%{_unitdir}/gluster-ta-volume.service
%endif

%if ( 0%{!?_without_georeplication:1} )
%files geo-replication
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfs-georep

%{_sbindir}/gfind_missing_files
%{_sbindir}/gluster-mountbroker
%dir %{_libexecdir}/glusterfs
%dir %{_libexecdir}/glusterfs/python
%dir %{_libexecdir}/glusterfs/python/syncdaemon
     %{_libexecdir}/glusterfs/gsyncd
     %{_libexecdir}/glusterfs/python/syncdaemon/*
%dir %{_libexecdir}/glusterfs/scripts
     %{_libexecdir}/glusterfs/scripts/get-gfid.sh
     %{_libexecdir}/glusterfs/scripts/secondary-upgrade.sh
     %{_libexecdir}/glusterfs/scripts/gsync-upgrade.sh
     %{_libexecdir}/glusterfs/scripts/generate-gfid-file.sh
     %{_libexecdir}/glusterfs/scripts/gsync-sync-gfid
     %{_libexecdir}/glusterfs/scripts/schedule_georep.py*
     %{_libexecdir}/glusterfs/gverify.sh
     %{_libexecdir}/glusterfs/set_geo_rep_pem_keys.sh
     %{_libexecdir}/glusterfs/peer_gsec_create
     %{_libexecdir}/glusterfs/peer_mountbroker
     %{_libexecdir}/glusterfs/peer_mountbroker.py*
     %{_libexecdir}/glusterfs/gfind_missing_files
     %{_libexecdir}/glusterfs/peer_georep-sshkey.py*
%{_sbindir}/gluster-georep-sshkey

       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/geo-replication
%ghost      %attr(0644,-,-) %{_sharedstatedir}/glusterd/geo-replication/gsyncd_template.conf
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create/post/S56glusterd-geo-rep-create-post.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create/pre

%endif

%files -n libglusterfs0
%{_libdir}/libglusterfs.so.*

%files -n libgfapi0
%{_libdir}/libgfapi.so.*
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/api.so

%files -n libgfchangelog0
%{_libdir}/libgfchangelog.so.*

%files -n libgfrpc0
%{_libdir}/libgfrpc.so.*

%files -n libgfxdr0
%{_libdir}/libgfxdr.so.*

%files -n python%{_pythonver}-gluster
# introducing glusterfs module in site packages.
# so that all other gluster submodules can reside in the same namespace.
%if ( %{_usepython3} )
%dir %{python3_sitelib}/gluster
     %{python3_sitelib}/gluster/__init__.*
     %{python3_sitelib}/gluster/__pycache__
     %{python3_sitelib}/gluster/cliutils
%else
%dir %{python2_sitelib}/gluster
     %{python2_sitelib}/gluster/__init__.*
     %{python2_sitelib}/gluster/cliutils
%endif

%files regression-tests
%dir %{_datadir}/glusterfs
     %{_datadir}/glusterfs/run-tests.sh
     %{_datadir}/glusterfs/tests
%exclude %{_datadir}/glusterfs/tests/vagrant

%if ( 0%{!?_without_server:1} )
%files ganesha
%dir %{_libexecdir}/ganesha
%{_sysconfdir}/ganesha/ganesha-ha.conf.sample
%{_libexecdir}/ganesha/*
%{_prefix}/lib/ocf/resource.d/heartbeat/*
%{_sharedstatedir}/glusterd/hooks/1/start/post/S31ganesha-start.sh
%ghost      %attr(0644,-,-) %config(noreplace) %{_sysconfdir}/ganesha/ganesha-ha.conf
%ghost %dir %attr(0755,-,-) %{_localstatedir}/run/gluster/shared_storage/nfs-ganesha
%ghost      %attr(0644,-,-) %config(noreplace) %{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha.conf
%ghost      %attr(0644,-,-) %config(noreplace) %{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha-ha.conf
%endif

%if ( 0%{!?_without_ocf:1} )
%files resource-agents
# /usr/lib is the standard for OCF, also on x86_64
%{_prefix}/lib/ocf/resource.d/glusterfs
%endif

%if ( 0%{!?_without_server:1} )
%files server
%doc extras/clear_xattrs.sh
# sysconf
%config(noreplace) %{_sysconfdir}/glusterfs
%exclude %{_sysconfdir}/glusterfs/thin-arbiter.vol
%exclude %{_sysconfdir}/glusterfs/eventsconfig.json
%exclude %{_sharedstatedir}/glusterd/nfs/nfs-server.vol
%exclude %{_sharedstatedir}/glusterd/nfs/run/nfs.pid
%if ( 0%{?_with_gnfs:1} )
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/nfs/*
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/glusterd
%if ( 0%{_for_fedora_koji_builds} )
%config(noreplace) %{_sysconfdir}/sysconfig/glusterfsd
%endif

# init files
%glusterd_svcfile
%if ( 0%{_for_fedora_koji_builds} )
%glusterfsd_svcfile
%endif
%if ( 0%{?_with_systemd:1} )
%glusterfssharedstorage_svcfile
%endif

# binaries
%{_sbindir}/glusterd
%{_libexecdir}/glusterfs/glfsheal
%{_sbindir}/gf_attach
%{_sbindir}/gluster-setgfid2path
# {_sbindir}/glusterfsd is the actual binary, but glusterfs (client) is a
# symlink. The binary itself (and symlink) are part of the glusterfs-fuse
# package, because glusterfs-server depends on that anyway.

# Manpages
%{_mandir}/man8/gluster-setgfid2path.8*

# xlators
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/arbiter.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/bit-rot.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/bitrot-stub.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/sdfs.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/index.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/locks.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/posix*
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/snapview-server.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/marker.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/simple-quota.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/quota*
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/selinux.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/trash.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/upcall.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/leases.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mgmt
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mgmt/glusterd.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol/server.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/storage
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/storage/posix.so

# snap_scheduler
%{_sbindir}/snap_scheduler.py
%{_sbindir}/gcron.py
%{_sbindir}/conf.py

# /var/lib/glusterd, e.g. hookscripts, etc.
%ghost      %attr(0644,-,-) %config(noreplace) %{_sharedstatedir}/glusterd/glusterd.info
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/bitd
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/groups
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/virt
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/metadata-cache
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/gluster-block
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/nl-cache
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/db-workload
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/distributed-virt
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/samba
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/glusterfind
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/glusterfind/.keys
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/glustershd
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post/disabled-quota-root-xattr-heal.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post/S10selinux-label-brick.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post/S13create-subdir-mounts.sh
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/pre
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/pre/S28Quota-enable-root-xattr-heal.sh
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create/post/S10selinux-label-brick.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/copy-file
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/copy-file/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/copy-file/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete/post
                            %{_sharedstatedir}/glusterd/hooks/1/delete/post/S57glusterfind-delete-post
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete/pre
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete/pre/S10selinux-del-fcontext.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/reset
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/reset/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/reset/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/post/S30samba-set.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/post/S32gluster_enable_shared_storage.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/post/S29CTDBsetup.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/post/S30samba-start.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/post
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/pre
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/pre/S30samba-stop.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/pre/S29CTDB-teardown.sh
%config(noreplace) %ghost      %attr(0600,-,-) %{_sharedstatedir}/glusterd/options
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/peers
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/quotad
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/scrub
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/snaps
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/ss_brick
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/vols

# Extra utility script
%dir %{_libexecdir}/glusterfs
%dir %{_datadir}/glusterfs/scripts
     %{_datadir}/glusterfs/scripts/stop-all-gluster-processes.sh
%if ( 0%{?_with_systemd:1} )
     %{_libexecdir}/glusterfs/mount-shared-storage.sh
     %{_datadir}/glusterfs/scripts/control-cpu-load.sh
     %{_datadir}/glusterfs/scripts/control-mem.sh
%endif

# Incrementalapi
     %{_libexecdir}/glusterfs/glusterfind
%{_bindir}/glusterfind
     %{_libexecdir}/glusterfs/peer_add_secret_pub

%if ( 0%{?_with_firewalld:1} )
%{_prefix}/lib/firewalld/services/glusterfs.xml
%endif
# end of server files
%endif

# Events
%if ( 0%{!?_without_events:1} )
%files events
%config(noreplace) %{_sysconfdir}/glusterfs/eventsconfig.json
%dir %{_sharedstatedir}/glusterd
%dir %{_sharedstatedir}/glusterd/events
%dir %{_libexecdir}/glusterfs
     %{_libexecdir}/glusterfs/gfevents
     %{_libexecdir}/glusterfs/peer_eventsapi.py*
%{_sbindir}/glustereventsd
%{_sbindir}/gluster-eventsapi
%{_datadir}/glusterfs/scripts/eventsdash.py*
%if ( 0%{?_with_systemd:1} )
%{_unitdir}/glustereventsd.service
%else
%{_sysconfdir}/init.d/glustereventsd
%endif
%endif

%changelog
* Tue Feb 06 2024 Yann Dirson <yann.dirson@vates.tech> - 11.1-1
- Update to version 11.1

* Fri Feb 02 2023 Yann Dirson <yann.dirson@vates.tech> - 9.6-1
- Update to version 9.6
- Force using python3 on 8.3

* Fri Sep 30 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 9.4-2
- Rebuild for XCP-ng 8.3

* Wed Dec 01 2021 Gael Duperrey <gduperrey@vates.fr> - 9.4-1
- Update to version 9.4

* Tue Nov 24 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2-1
- Update to version 8.2

* Wed Sep 09 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.1-1
- Update to version 8.1
