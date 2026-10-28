#!/bin/sh -e
#
# make-cacerts.sh
#
# based on:
#
# update-ca-certificates
#
# Copyright (c) 2003 Fumitoshi UKAI <ukai@debian.or.jp>
# Copyright (c) 2009 Philipp Kern <pkern@debian.org>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02111-1301,
# USA.
#

# the spec runs this script through sh, which ignores -e on the #! line
set -e

verbose=0
DESTDIR=
while [ $# -gt 0 ];
do
  case $1 in
  --verbose|-v)
  	verbose=1;;
  --destdir)
	DESTDIR=$2; shift;;
  --help|-h|*)
	echo "$0: [--verbose]"
	exit;;
  esac
  shift
done

CERTSCONF=$DESTDIR/etc/ca-certificates.conf
CERTSCONFD=$DESTDIR/etc/ca-certificates.d
CERTSDIR=$DESTDIR/usr/share/ca-certificates
LOCALCERTSDIR=$DESTDIR/etc/certs
CERTBUNDLE=$DESTDIR/etc/certs/ca-certificates.crt
ETCCERTSDIR=$DESTDIR/etc/openssl/certs

KEYSTORE=$PWD/cacerts
KEYTOOL=$PWD/tmp-bin/keytool

export LC_ALL=C.utf-8

# Roots OpenJDK dropped from its own cacerts (JDK-8395690, CVE-2026-114820);
# keep them out of ours even while the system bundle still trusts them.
distrusted() {
  fp=$($KEYTOOL -printcert -file "$1" | sed -n 's/^[[:space:]]*SHA256: //p')
  if [ -z "$fp" ]; then
    echo "E: cannot read the SHA256 fingerprint of $1" >&2
    exit 1
  fi
  case "$fp" in
  D7:A7:A0:FB:5D:7E:27:31:D7:71:E9:48:4E:BC:DE:F7:1D:5F:0C:3E:0A:29:48:78:2B:C8:3E:E0:EA:69:9E:F4) return 0;; # AAA Certificate Services
  86:A1:EC:BA:08:9C:4A:8D:3B:BE:27:34:C6:12:BA:34:1D:81:3E:04:3C:F9:E8:A8:62:CD:5C:57:A3:6B:BE:6B) return 0;; # emSign ECC Root CA - G3
  40:F6:AF:03:46:A9:9A:A1:CD:1D:55:5A:4E:9C:CE:62:C7:F9:63:46:03:EE:40:66:15:83:3D:C8:C8:D0:03:67) return 0;; # emSign Root CA - G1
  1A:A0:C2:70:9E:83:1B:D6:E3:B5:12:9A:00:BA:41:F7:EE:EF:02:08:72:F1:E6:50:4B:F0:F6:C3:F2:4F:3A:F3) return 0;; # emSign Root CA - G2
  esac
  return 1
}

# Adds a certificate to the list of trusted ones.
# Adds the certificate to the cacerts file
add() {
  CERT="$1"
  NAME="$2"

  if distrusted "$CERT"; then
    echo "  skipping distrusted '$CERT'"
    return
  fi
  ALIAS="$(echo "$NAME" | sed -e 's/.\(crt|pem\)$//' -e 's/ /_/g' \
                                                -e 's/[()]/=/g' -e 's/,/_/g')"

  if [ "$verbose" = 1 ] ; then
    echo "  adding '$CERT' as '$ALIAS'"
  fi
  if ! $KEYTOOL -noprompt -import -alias "$ALIAS" \
                -keystore $KEYSTORE -storepass 'changeit' \
                -file "$CERT" ; then
        echo "W: $NAME certification could not be added"
  fi 
}

cd $ETCCERTSDIR

for conf in $CERTSCONF $CERTSCONFD/*.conf; do
  # skip inexistent files (matched by glob)
  [ -f $conf ] || continue

  sed -e '/^$/d' -e '/^#/d' -e '/^!/d' $conf | while read crt
  do
    if test -f "$CERTSDIR/$crt"
    then
      add "$CERTSDIR/$crt" "$crt"
    elif test -f "$LOCALCERTSDIR/$crt"
    then
      add "$LOCALCERTSDIR/$crt" "$crt"
    else
      echo "W: $CERTSDIR/$crt or $LOCALCERTSDIR/$crt not found, but listed in $conf." >&2
      continue
    fi
  done
done

echo "done."

# vim:set et sw=2:

