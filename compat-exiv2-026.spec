
Name:    compat-exiv2-026
Version: 0.26
Release: 1%{?dist}
Summary: Compatibility package with the exiv2 library in version 0.26

License: GPLv2+
URL:     http://www.exiv2.org/
Source0: http://www.exiv2.org/builds/exiv2-%{version}-trunk.tar.gz

## upstream patches
Patch6:  0006-1296-Fix-submitted.patch

Patch10: exiv2-CVE-2017-17723.patch
Patch11: exiv2-CVE-2017-17725.patch
Patch12: exiv2-CVE-2017-5772.patch

BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libcurl)
BuildRequires: zlib-devel

Conflicts: exiv2-libs < 0.27

%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments


%prep
%autosetup -n exiv2-trunk -p1


%build
# exiv2: embedded copy of exempi should be compiled with BanAllEntityUsage
# https://bugzilla.redhat.com/show_bug.cgi?id=888769
export CPPFLAGS="-DBanAllEntityUsage=1"

%configure \
  --disable-rpath \
  --disable-static

# rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

## Unpackaged files
rm -rf %{buildroot}%{_bindir}/exiv2
rm -rf %{buildroot}%{_libdir}/libexiv2.la
rm -rf %{buildroot}%{_datadir}/locale/*
rm -rf %{buildroot}%{_mandir}/*
rm -rf %{buildroot}%{_libdir}/pkgconfig/exiv2.pc
rm -rf %{buildroot}%{_includedir}/exiv2
rm -rf mv %{buildroot}%{_libdir}/libexiv2.so

## fix perms on installed lib
ls -l     %{buildroot}%{_libdir}/libexiv2.so.*
chmod 755 %{buildroot}%{_libdir}/libexiv2.so.*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README
%{_libdir}/libexiv2.so.26*


%changelog
* Tue Jan 29 2019 Jan Grulich <jgrulich@redhat.com> - 0.26-1
- Spec file based on exiv2 package to provide old libraries before API change
  Resolves: bz#1668355

