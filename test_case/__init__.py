# __author:"zonglr"
# date:2020/5/23
#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
from __future__ import absolute_import
#
import os
import sys

aa = os.path.abspath(os.path.join(os.path.dirname(__file__))) + '\\common'
sys.path.append(aa)
bb = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(bb)
cc = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(cc)