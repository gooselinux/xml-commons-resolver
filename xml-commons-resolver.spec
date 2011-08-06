%define gcj_support 1

Name:           xml-commons-resolver
Version:        1.1
Release:        4.18%{?dist}
Epoch:          0
Summary:        Resolver subproject of xml-commons
License:        ASL 1.1
URL:            http://xml.apache.org/commons/
Source0:        http://www.apache.org/dist/xml/commons/xml-commons-resolver-1.1.tar.gz
Source1:        xml-commons-resolver-resolver.sh
Source2:        xml-commons-resolver-xread.sh
Source3:        xml-commons-resolver-xparse.sh
Source4:        %{name}-MANIFEST.MF

Patch0:         %{name}-src-version.patch

Requires:       jaxp_parser_impl
Requires:       xml-commons-apis
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  dos2unix
#BuildRequires:  %{_bindir}/xsltproc
#BuildRequires:  docbook-style-xsl
Group:          Development/Libraries
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description
Resolver subproject of xml-commons.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
# for /bin/rm and /bin/ln
Requires(post):   coreutils
Requires(postun): coreutils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

%patch0

# remove all binary libs and prebuilt javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf docs
dos2unix KEYS LICENSE.resolver.txt

%build
perl -p -i -e 's|call Resolver|call resolver|g' resolver.xml
perl -p -i -e 's|classname="org.apache.xml.resolver.Catalog"|fork="yes" classname="org.apache.xml.resolver.apps.resolver"|g' resolver.xml
perl -p -i -e 's|org.apache.xml.resolver.Catalog|org.apache.xml.resolver.apps.resolver|g' src/manifest.resolver
#DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep /html/docbook.xsl \
#| sed 's#html/docbook.xsl##'`
#
#if [ -z $DOCBOOK_XSL ]; then
#  echo "Unable to find docbook xsl directory"
#  exit 1
#fi

#ant -Ddocbook.dir=$DOCBOOK_XSL -f resolver.xml main
ant -f resolver.xml jar javadocs

%install
rm -rf $RPM_BUILD_ROOT

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE4} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/resolver.jar META-INF/MANIFEST.MF

# Jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp build/resolver.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

# Jar versioning
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# Javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/apidocs/resolver/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/xml-resolver
cp %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/xml-xread
cp %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/xml-xparse

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%post
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc KEYS LICENSE.resolver.txt
%{_javadir}/*
%attr(0755,root,root) %{_bindir}/*

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.1-4.18
- Fix Group tags
- Remove '.' at end of Summary
- Add dos2unix BR and fix line endings

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.1-4.17
- Rebuilt for RHEL 6

* Sat Aug  8 2009 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1-4.16
- Fix specfile UTF-8 encoding.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-4.15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-3.15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-2.15
- Install osgi manifest for eclipse-dtp

* Fri Sep 05 2008 Deepak Bhole <dbhole@redhat.com> 1.1-2.14
- Build with IcedTea to escape sinjdoc issues

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1-2.13
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.1-2jpp.12
- Autorebuild for GCC 4.3

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> 1.1-1jpp.12
- Added missing dependencies.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.1-1jpp_11fc
- Rebuilt

* Fri Jul 21 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.1-1jpp_10fc
- Added conditional native compilation.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.1-1jpp_9fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.1-1jpp_8fc
- stop scriptlet spew

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:1.1-1jpp_7fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0:1.1-1jpp_6fc
- rebuilt

* Tue Jun 28 2005 Gary Benson <gbenson@redhat.com> 0:1.1-1jpp_5fc
- Remove jarfile from the tarball.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:1.1-1jpp_4fc
- Build into Fedora.

* Thu Oct 28 2004 Gary Benson <gbenson@redhat.com> 0:1.1-1jpp_3fc
- Bootstrap into Fedora.

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 0:1.1-1jpp_2rh
- RH vacuuming part II

* Wed Mar  3 2004 Frank Ch. Eigler <fche@redhat.com> 0:1.1-1jpp_1rh
- RH vacuuming

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.1-1jpp
- 1.1
- use perl instead of patch
- don't build docs (build fails)

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.0-2jpp
- update for JPackage 1.5

* Wed Nov 13 2002 Ville Skyttä <ville.skytta at iki.fi> - 1.0-1jpp
- Follow upstream changes, split out of xml-commons.
