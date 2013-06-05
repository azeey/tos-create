#!/usr/bin/env python
# encoding: utf-8

# @author: Addisu Z. Taddese
# Script to generate a small tinyos app/project. The script generates a module
# and configuration based on a project name passed on the command line
#

import os
import argparse

makefile_tmpl = '''
COMPONENT={app_name}
include $(MAKERULES)
'''

app_tmpl = '''
configuration {app_name}{{
}}
implementation {{
  components {module_name}, MainC;

  {module_name} -> MainC.Boot;
}}

'''

module_tmpl = '''
module {module_name} {{
  uses {{
    interface Boot;
  }}


}}
implementation {{

  event void Boot.booted(){{
  }}

}}
'''

creation_list = (
    (makefile_tmpl, 'Makefile'),
    (app_tmpl, '{app_name}.nc'),
    (module_tmpl, '{module_name}.nc'),
)

def main():
    """Main program
    :returns: None

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('project', help='Project name')
    parser.add_argument('-d', dest='outdir', default='.', help='Output directory')

    args = parser.parse_args()

    # Create project variables
    variables = {
        'app_name' : "{project_name}AppC",
        'module_name' : "{project_name}C",
    }
    # Populate variables
    for key in variables:
        variables[key] = variables[key].format(project_name=args.project)

    # Make project directory
    project_dir = os.path.join(args.outdir, args.project)
    os.mkdir(project_dir)

    # Render templates and createfiles
    for tmpl, filename in creation_list:
        outfile = os.path.join(project_dir, filename.format(**variables))
        rendered = tmpl.format(**variables)

        print "Creating", outfile
        with open(outfile, 'w') as f:
            f.write(rendered)

if __name__ == '__main__':
    main()
