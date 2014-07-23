import urllib2
import re
import os

response = urllib2.urlopen('http://downloads.activestate.com/Komodo/nightly/komodoide/latest-trunk/SHA1SUM').read()


packages = response.split("\n")
replaces = {
	'VERSION': 0,
	'SHA1SUM_x86': 0,
	'SHA1SUM_x86_64': 0,
}
for package in packages:
	if package == '' or not package.endswith('.tar.gz'):
		continue
	sha1sum, filename = package.split('  ')
	matches = re.match(r'Komodo-IDE-([0-9a-z-.]+)-linux-(x86(_64)?).tar.gz', filename)
	version = matches.group(1).replace('-', '_')
	architecture = matches.group(2)
	replaces['VERSION'] = version
	replaces['SHA1SUM_'+architecture] = sha1sum

templateFile = open('PKGBUILD.tmpl')
template = templateFile.read()
templateFile.close()
for search, replace in replaces.iteritems():
	template = template.replace('{{'+search+'}}', replace)

oldbuild = open('PKGBUILD', 'r')
if template == oldbuild.read():
	print "No build changes."
else:
	pkgbuild = open('PKGBUILD', 'w+')
	pkgbuild.write(template)
	pkgbuild.close()
	os.system('mkaurball')
	os.system('burp komodo-ide-nightly-'+version+'-1.src.tar.gz')
	
