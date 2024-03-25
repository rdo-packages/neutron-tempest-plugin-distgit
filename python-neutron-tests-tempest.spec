%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global service neutron
%global plugin neutron-tempest-plugin
%global module neutron_tempest_plugin
%global with_doc 1


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global common_desc \
This package contains Tempest tests to cover the Neutron project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of Neutron Project
License:    Apache-2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{service}-tests-tempest
Summary: %{summary}

Provides: python3-networking-bgpvpn-tests-tempest = %{version}-%{release}
Provides: python-networking-bgpvpn-tests-tempest = %{version}-%{release}
Obsoletes: python3-networking-bgpvpn-tests-tempest

Provides: python3-networking-sfc-tests-tempest = 9.0.0-%{release}
Provides: python-networking-sfc-tests-tempest = 9.0.0-%{release}
Obsoletes: python3-networking-sfc-tests-tempest < 9.0.0

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires:   nmap

%description -n python3-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        Documentation for python-%{service}-tests-tempest

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron tempest plugin.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{plugin}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e docs
%else
  %pyproject_buildrequires -R
%endif

%build
%pyproject_wheel

# Generate Docs
%if 0%{?with_doc}
export PYTHONPATH=.
%tox -e docs
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
# REMOVEME: error caused by commit https://opendev.org/openstack/neutron-tempest-plugin/commit/7e3ba069dc8d75ad0a8dcfed230766bdec5faafb
