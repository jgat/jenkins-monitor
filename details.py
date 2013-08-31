#!/usr/bin/env python
"""Get all the details"""

import sys
import pprint

from monitor import get

if __name__ == '__main__':
    base_url = sys.argv[1]
    info = get(base_url)
    pprint.pprint(info)
    print '\n\n'

    num = info['lastCompletedBuild']['number'] if len(sys.argv) < 3 else sys.argv[2]

    last_url = "{0}/{1}".format(base_url, num)
    last = get(last_url)
    pprint.pprint(last)
