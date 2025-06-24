%if "%{?buildtype}" == "" || "%{buildtype}" == "test"
... test-related RPM stuff ...
%endif

%if "%{?buildtype}" == "" || "%{buildtype}" == "server"
... server-related RPM stuff ...
%endif