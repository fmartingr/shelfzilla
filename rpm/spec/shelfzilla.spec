Summary: Shelfzilla
Name: Shelfzilla
Version: %{_gs_version}
Release: %{_gs_revision}
BuildRoot: %{_topdir}/BUILD/%{name}
BuildArch: noarch
Provides: shelfzilla
Requires: python27
License:  
Group: FDB
Distribution: FDB Global Services
Vendor: FDB 

%description
Shelfzilla is a website which save all your Manga

%defina _app_dir /opt/shelfzilla
%define _binaries_in_noarch_packages_terminate_build 0

# Do not check unpackaged files
%undefine __check_files

# -------------------------------------------------------------------------------------------- #
# prep section:
# -------------------------------------------------------------------------------------------- #
# Remove previous build files
%prep
rm -rf  $RPM_BUILD_ROOT*
[ -d $RPM_BUILD_ROOT%{_app_dir} ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}


# -------------------------------------------------------------------------------------------- #
# install section:
# -------------------------------------------------------------------------------------------- #
%install
# Copy Source Code
cp -r %{_gitdir}/* $RPM_BUILD_ROOT%{_app_dir} 


# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post
## Npm install
## pip install
## Syncdb dir manage
## migrate
## grunt compile
## python2.7 manage.py collectstatic

 





# -------------------------------------------------------------------------------------------- #
# pre-uninstall section:
# -------------------------------------------------------------------------------------------- #
%preun


# -------------------------------------------------------------------------------------------- #
# post-uninstall section:
# -------------------------------------------------------------------------------------------- #
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_app_dir}/*


