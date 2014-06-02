naglib
===

A configuration library for nagios

Background
---

First some background. I have been monitoring systems with nagios for nearly 10
years. Every time I switch jobs I end up wishing I had a nagios setup like we
had at my previous job. I usually end up rewriting a configuration script very
similar to this one, mostly from memory.


I am sure there is better stuff out there to configure nagios. I like my way. :)

Install
---

naglib is packaged as a python module. Take it for a spin:

        virtualenv env # optionally create a virtualenv
        ./env/bin/pip install naglib
        ./env/bin/naglib_generate -c naglib/fixtures/naglib.yml

Configure
---

Currently, the configuration is in the form of a yaml file. Look at the example
file included in the repo. Hopefully it's obvious, if not:

  * output: specify where to write the nagios config
  * prefix: path to static nagios configs, e.g. templates
  * engine: currently only ReClassifier
  * ReClassifier: configuration for the ReClassifier engine


ReClassifier Engine
---

The ReClassifier engine consumes a list of hosts from a csv file and determines
which services to configure based on regular expression matching against the
fields in the csv file.

  * csv: the csv file containing the hosts to monitor
  * host_mappings: map fields in the csv to any attribute supported by nagios
  * rules: a collection of rules that configure checks when matched
    * re: the regular expression to match against the field
    * field: the field number to match against
    * checks: a list of checks to apply when the check matches


Nagios
---

You still need to configure nagios. You should run the `naglib_generate` script
on the nagios master with the output location set to somewhere nagios can read,
e.g. /etc/nagios/build. Then make sure you include the build directories in the
main nagios.cfg file.

As it currently stands naglib expects to be able to read pre-existing
host/service template files. The files must contain a single object per file so
that naglib can read them.


Contribute
---

Please do. Send me a PR. There is still quite a lot of rough edges in naglib.

Thanks
---

That's all! Thanks for taking the time to check out naglib.
