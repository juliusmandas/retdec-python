#!/usr/bin/env python
#
# A script for analysis of binary files by using the retdec.com public REST API
# (https://retdec.com/api/). Internally, it uses the retdec-python library
# (https://github.com/s3rvac/retdec-python), which is assumed to be installed
# and available for import.
#
# Copyright: (c) 2015 by Petr Zemek <s3rvac@gmail.com> and contributors
# License: MIT, see the LICENSE file for more details
#

import sys

# Allow running the script from the root repository path, i.e. by executing
# `scripts/fileinfo.py`. If we did not include the current working
# directory into the path, the 'retdec' package would not be found.
sys.path.append('.')

from retdec.tools import fileinfo

if __name__ == '__main__':
    try:
        sys.exit(fileinfo.main())
    except Exception as ex:
        sys.stderr.write('error: {}\n'.format(str(ex)))
        sys.exit(1)
