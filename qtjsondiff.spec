# spectool -g -R qtjsondiff.spec
# rpmbuild -ba qtjsondiff.spec

%define name QTjsonDiff
%define reponame qtjsondiff
%define version %(echo "$(curl --silent 'https://raw.githubusercontent.com/coozoo/qtjsondiff/master/main.cpp'|grep -oP '(?<=const QString APP_VERSION=\").*(?=\";)')")
%define build_timestamp %{lua: print(os.date("%Y%m%d"))}

Summary: QT json diff UI viwer
Name: %{name}
Version: %{version}
Release: %{build_timestamp}
Source0: https://github.com/coozoo/qtjsondiff/archive/master.zip#/%{name}-%{version}-%{release}.tar.gz


License: MIT

%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
BuildRequires: qt5-qtbase-devel >= 5.12
BuildRequires: qt5-linguist >= 5.12
BuildRequires: zlib-devel
%endif
%if 0%{?mageia} || 0%{?suse_version}
Group:          Development/Tools/Other
Url:            https://github.com/coozoo/qtjsondiff
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  libqt5-qtbase-devel
BuildRequires:  libqt5-linguist
BuildRequires:  update-desktop-files
BuildRequires:  zlib-devel
Requires(post): update-desktop-files
Requires(postun): update-desktop-files
%endif

# Requires: qt5 >= 5.11

Url: https://github.com/coozoo/qtjsondiff

%description

Some kind of diff viewer for Json that consists of two json viewer widgets.
There is two modes to view:
json and text, search text inside json. Use different sources
of json file, url or simply copy-paste. And some more features.

%global debug_package %{nil}

%prep
#copr build
%setup -q -n %{name}-%{version}
#local build
#%setup -q -n %{reponame}-master

%build
# don't know maybe it's stupid me but lrelease in qt looks like runs after make file generation as result automatic file list inside qmake doesn't work
# so what I need just run it twice...
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
    qmake-qt5
    make
    qmake-qt5
    make
%endif
%if 0%{?mageia} || 0%{?suse_version}
    %qmake5
    %make_build
    %qmake5
    %make_build
%endif

%install
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
    make INSTALL_ROOT=%{buildroot} -j$(nproc) install
%endif
%if 0%{?mageia} || 0%{?suse_version}
    mkdir %{buildroot}/%{_datadir}/pixmaps
    mv %{buildroot}/%{_datadir}/icons/diff.png %{buildroot}/%{_datadir}/pixmaps/diff.png
    %suse_update_desktop_file -G "JSON Diff Tool" -r qtjsondiff Utility TextEditor
%endif

%post
%if 0%{?mageia} || 0%{?suse_version}
    %desktop_database_post
%endif

%postun
%if 0%{?mageia} || 0%{?suse_version}
    %desktop_database_postun
%endif


%files
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
    %{_bindir}/*
    %{_datadir}/*
%endif
%if 0%{?mageia} || 0%{?suse_version}
    %license LICENSE
    %doc README.md
    %{_bindir}/%{name}
    %{_datadir}/pixmaps/diff.png
    %{_datadir}/applications/qtjsondiff.desktop
%endif    

%changelog
