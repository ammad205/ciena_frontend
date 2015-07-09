#!/usr/bin/env python
import json
import time
class ModelerTest():
        def main_func(self,json_str):
            with open("testmodeler_output.txt", "w") as f:
                    print(json_str)
                    f.write(str(json_str)+ "\n")

          



