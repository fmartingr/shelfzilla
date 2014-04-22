Summary: Shelfzilla
Name: shelfzilla
Version: %{_gs_version}
Release: %{_gs_revision}
BuildRoot: %{_topdir}/BUILD/%{name}
BuildArch: x86_64
Provides: shelfzilla
Requires: python27
License:  Comercial
Group: FDB
Distribution: FDB Global Services
Vendor: FDB 

%description
Shelfzilla is a website which save all your Manga

%define _app_dir /opt/shelfzilla
%define _binaries_in_noarch_packages_terminate_build 0

# Do not check unpackaged files
%undefine __check_files

# -------------------------------------------------------------------------------------------- #
# prep section:
# -------------------------------------------------------------------------------------------- #
# Remove previous build files
%prep
rm -rf  $RPM_BUILD_ROOT*

# clean up development-only files
find %{_gitdir} -depth -name .git -exec rm -rf {} \;

# -------------------------------------------------------------------------------------------- #
# install section:
# -------------------------------------------------------------------------------------------- #
%install
# Make structure
[ -d $RPM_BUILD_ROOT%{_app_dir} ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}
[ -d $RPM_BUILD_ROOT%{_app_dir}/config ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}/config
[ -d $RPM_BUILD_ROOT%{_app_dir}/static_components ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}/static_components

# Copy Source Code
cp -r %{_gitdir}/shelfzilla $RPM_BUILD_ROOT%{_app_dir}
cp -r %{_gitdir}/config/production $RPM_BUILD_ROOT%{_app_dir}/config
cp -r %{_gitdir}/config/requirements.txt $RPM_BUILD_ROOT%{_app_dir}/config
cp -r %{_gitdir}/*.json $RPM_BUILD_ROOT%{_app_dir}/
cp -r %{_gitdir}/*.py $RPM_BUILD_ROOT%{_app_dir}/
cp -r %{_gitdir}/gruntfile.coffee $RPM_BUILD_ROOT%{_app_dir}/

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post
## Npm install
cd %{_app_dir} && npm install

## pip install
pip install -r %{_app_dir}/config/production/requirements.txt

## Syncdb dir manage
python2.7 %{_app_dir}/manage.py syncdb

## Migrate
python2.7 %{_app_dir}/manage.py migrate

## Bower
bower install --allow-root

## Grunt compile
cd %{_app_dir} && grunt compile

## Collect static
python2.7 manage.py collectstatic --clear --noinput

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


