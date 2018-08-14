%global snapdate 20180418
%global commit 27574518bb3be9f7c7fc060e6be39df6eac85f21
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global rel 3

# Replacing urpmi
%bcond_without as_urpmi

Name:           dnf-URPM
Version:        0
Release:        %{?snapdate:0.git%{snapdate}.%{shortcommit}.}%{rel}
Summary:        URPM* tool suite implemented on top of DNF

License:        GPLv3+
URL:            https://github.com/rpm-software-management/%{name}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  python3-devel
# dnf-urpmi
Requires:       dnf-command(install)
Requires:       dnf-command(upgrade)
Requires:       dnf-command(builddep)
Requires:       dnf-command(downgrade)
Requires:       dnf-command(reinstall)
# dnf-urpmi.update - Not yet implemented
#Requires:       dnf-command(makecache)
# dnf-urpme
Requires:       dnf-command(remove)
# dnf-urpmq / dnf-urpmf - Not yet implemented
#Requires:       dnf-command(repoquery)

Provides:       dnf-urpm = %{version}-%{release}

BuildArch:      noarch

%if %{with as_urpmi}
Obsoletes:      urpmi < 8.03.5
Provides:       urpmi = 8.03.5
%endif

%description
dnf-URPM aims to reimplement the URPM tool suite on top of DNF,
a next generation repository manager and dependency resolver with
a well-defined and tested CLI and API.

The hope is to implement as much of the functionality of urpmi,
urpmi.update, urpme, urpmq, and urpmf as possible on top of DNF.


%prep
%autosetup -n %{name}-%{commit}

%build
# Nothing to build

%install
# Install module code
mkdir -p %{buildroot}%{python3_sitelib}
cp -av dnf_URPM %{buildroot}%{python3_sitelib}

# Install commands
mkdir -p %{buildroot}%{_bindir}
%if %{with as_urpmi}
mkdir -p %{buildroot}%{_sbindir}
%endif

for urpmcmd in urpmi urpme; do
    install -pm 0755 dnf-${urpmcmd} %{buildroot}%{_bindir}/dnf-${urpmcmd}
%if %{with as_urpmi}
    ln -sr %{buildroot}%{_bindir}/dnf-${urpmcmd} %{buildroot}%{_sbindir}/${urpmcmd}
%endif
done


%files
%license LICENSE
%doc README.md AUTHORS.md TODO.md
%{python3_sitelib}/dnf_URPM/
%{_bindir}/dnf-urpm*
%if %{with as_urpmi}
%{_sbindir}/urpm*
%endif


