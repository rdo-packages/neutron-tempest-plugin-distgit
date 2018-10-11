%global service neutron
%global plugin neutron-tempest-plugin
%global module neutron_tempest_plugin
%global with_doc 1

# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%global with_python3 1
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This package contains Tempest tests to cover the Neutron project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       %{pyver_bin}-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of Neutron Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n %{pyver_bin}-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide %{pyver_bin}-%{service}-tests-tempest}

Obsoletes: %{pyver}-neutron-tests < 1:12.0.0

BuildRequires:  %{pyver_bin}-devel
BuildRequires:  %{pyver_bin}-pbr
BuildRequires:  %{pyver_bin}-setuptools

Requires:   %{pyver_bin}-ddt >= 1.0.1
Requires:   %{pyver_bin}-eventlet >= 0.20.1
%if 0%{?fedora} > 0
Requires:   %{pyver_bin}-netaddr >= 0.7.19
%else
Requires:   python-ipaddress
Requires:   python-netaddr >= 0.7.19
%endif
Requires:   %{pyver_bin}-neutron-lib >= 1.13.0
Requires:   %{pyver_bin}-oslo-config >= 2:5.2.0
Requires:   %{pyver_bin}-oslo-log >= 3.36.0
Requires:   %{pyver_bin}-oslo-serialization >= 2.18.0
Requires:   %{pyver_bin}-oslo-utils >= 3.33.0
Requires:   %{pyver_bin}-pbr >= 3.3.1
Requires:   %{pyver_bin}-six  >= 1.10.0
Requires:   %{pyver_bin}-tempest >= 1:18.0.0
Requires:   %{pyver_bin}-testtools >= 1.8.0
Requires:   %{pyver_bin}-testscenarios >= 0.5.0

%description -n %{pyver_bin}-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n %{pyver_bin}-%{service}-tests-tempest-doc
Summary:        %{pyver_bin}-%{service}-tests-tempest documentation

BuildRequires:  %{pyver_bin}-sphinx
BuildRequires:  %{pyver_bin}-openstackdocstheme

%description -n %{pyver_bin}-%{service}-tests-tempest-doc
It contains the documentation for the Neutron tempest plugin.
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n %{pyver_bin}-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n %{pyver_bin}-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
