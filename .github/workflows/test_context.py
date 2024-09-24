# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2023 The SPDX Contributors

import sys
from rdflib import Graph


def parseString(data: str) -> Graph:
    return Graph().parse(data=data, format="json-ld")


def testLocalContext(context_file: str) -> Graph:
    data = '{ "@context": [ "' + context_file + '" ], "@graph": [ ] }'
    return parseString(data)


if __name__ == "__main__":
    # run testLocalContext with first argument as context file
    testLocalContext(sys.argv[1])
