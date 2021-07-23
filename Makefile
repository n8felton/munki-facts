USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make
TITLE=munki-facts
REVERSE_DOMAIN=edu.rit
PACKAGE_VERSION=$(shell date +"%Y.%m.%d")
PACKAGE_MAJOR_VERSION=$(shell date +"%y")
PACKAGE_MINOR_VERSION=$(shell date +"%m")
PAYLOAD=\
		pack-munki-facts

pack-munki-facts: munki_facts.py facts
		@sudo mkdir -p ${WORK_D}/usr/local/munki/conditions/facts
		@sudo ${CP} ./munki_facts.py ${WORK_D}/usr/local/munki/conditions
		@sudo ${DITTO} ./facts ${WORK_D}/usr/local/munki/conditions/facts
		@sudo chown -R root:wheel ${WORK_D}/usr/local/munki/conditions
		@sudo chmod -R 755 ${WORK_D}/usr/local/munki/conditions
