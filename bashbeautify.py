#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**************************************************************************
#   Copyright (C) 2011, Paul Lutus                                        *
#                                                                         *
#   This program is free software; you can redistribute it and/or modify  *
#   it under the terms of the GNU General Public License as published by  *
#   the Free Software Foundation; either version 2 of the License, or     *
#   (at your option) any later version.                                   *
#                                                                         *
#   This program is distributed in the hope that it will be useful,       *
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#   GNU General Public License for more details.                          *
#                                                                         *
#   You should have received a copy of the GNU General Public License     *
#   along with this program; if not, write to the                         *
#   Free Software Foundation, Inc.,                                       *
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
#**************************************************************************

import re, sys
import argparse

PVERSION = '1.0'

class BeautifyBash:

  def __init__(self):
    self.tab_str = ' '
    self.tab_size = 2
    self.do_backup = True

  def read_file(self,fp):
    with open(fp) as f:
      return f.read()

  def write_file(self,fp,data):
    with open(fp,'w') as f:
      f.write(data)

  def beautify_string(self,data,path = ''):
    tab = 0
    case_stack = []
    in_here_doc = False
    defer_ext_quote = False
    in_ext_quote = False
    continued = False
    ext_quote_string = ''
    here_string = ''
    last_if_indent = ''
    output = []
    line = 1
    for record in re.split('\n',data):
      record = record.rstrip()
      stripped_record = record.strip()

      # strip quotes from here-doc delimeter (<<-"NAME", etc)
      test_record = re.sub(r'(<<-?\s*)["\']((?:\\.|[^"\\])*?)["\']',r'\1\2',stripped_record)
      # collapse multiple quotes between ' ... '
      test_record = re.sub(r'\'.*?\'','',test_record)
      # collapse multiple quotes between " ... "
      test_record = re.sub(r'(?<!\\)"(\\.|[^"\\])*?"','',test_record)
      # collapse multiple quotes between ` ... `
      test_record = re.sub(r'`.*?`','',test_record)
      # collapse multiple quotes between \` ... ' (weird case)
      test_record = re.sub(r'\\`.*?\'','',test_record)
      # strip out any escaped single characters
      test_record = re.sub(r'\\.','',test_record)
      # remove '#' comments
      test_record = re.sub(r'(\A|\s)(#.*)','',test_record,1)
      # collapse ( ... ) or (( ... ))
      test_record = re.sub(r'\([^()]*(\([^()]*\))*[^()]*\)','',test_record)
      if(in_here_doc): # pass on with no changes
        output.append(record)
        # now test for here-doc termination string
        if(re.search(here_string,test_record) and not re.search('<<',test_record)):
          in_here_doc = False
      else: # not in here doc
        if(re.search('<<-?',test_record)):
          here_string = re.sub('.*<<-?\s*[\'|"]?([-_|\w]+)[\'|"]?.*','\\1',test_record,1)
          in_here_doc = (len(here_string) > 0)
        if(in_ext_quote):
          if(re.search(ext_quote_string,test_record)):
            # provide line after quotes
            test_record = re.sub('.*%s(.*)' % ext_quote_string,'\\1',test_record,1)
            in_ext_quote = False
        else: # not in ext quote
          if(re.search(r'(\A|\s)(\'|")',test_record)):
            # apply only after this line has been processed
            defer_ext_quote = True
            ext_quote_string = re.sub('.*([\'"]).*','\\1',test_record,1)
            # provide line before quote
            test_record = re.sub('(.*)%s.*' % ext_quote_string,'\\1',test_record,1)
        if(in_ext_quote):
          # pass on unchanged
          output.append(record)
        else: # not in ext quote
          inc = len(re.findall('(\s|\A|;)(case|then|do)(;|\Z|\s)',test_record))
          inc += len(re.findall('(\{|\(|\[)',test_record))
          outc = len(re.findall('(\s|\A|;)(esac|fi|done|elif)(;|\)|\||\Z|\s)',test_record))
          outc += len(re.findall('(\}|\)|\])',test_record))
          if(re.search(r'\besac\b',test_record)):
            if(len(case_stack) == 0):
              sys.stderr.write(
                'File %s: error: "esac" before "case" in line %d.\n' % (path,line)
              )
            else:
              outc += case_stack.pop()
          # sepcial handling for bad syntax within case ... esac
          if(len(case_stack) > 0):
            if(re.search('\A[^(]*\)',test_record)):
              # avoid overcount
              outc -= 2
              case_stack[-1] += 1
            if(re.search(';;',test_record)):
              outc += 1
              case_stack[-1] -= 1
          # an ad-hoc solution for the "else"/"elif" keyword
          else_case = (0,-1)[re.search(r'^(else\b|elif\b.*\bthen$)',test_record) != None]
          # an ad-hoc solution for the standalone ";;"
          double_comma_case = (0,+1)[re.search('^;;$',test_record) != None]
          net = inc - outc
          tab += min(net,0)
          extab = tab + else_case + double_comma_case
          extab = max(0,extab)
          if(continued):
            # pass on unchanged
            output.append(record)
          else:
            # indent the line unless it's empty
            if stripped_record:
              # fix up comment line aligned at the same column with following else or elif line
              if stripped_record.startswith('#') and last_if_indent == re.match(r'^\s*',record).group():
                extab = max(0, extab - 1)
              output.append((self.tab_str * self.tab_size * extab) + stripped_record)
            else:
              output.append('')
          tab += max(net,0)
        if(defer_ext_quote):
          in_ext_quote = True
          defer_ext_quote = False
        if(re.search(r'\bcase\b',test_record)):
          case_stack.append(0)
        # remember the indent of "if" or "elif"
        m = re.search(r'^(\s*)(if|elif|then)\b',record)
        if m:
          last_if_indent = m.group(1)
        elif re.search(r'^(\s*)(else|fi)\b',record):
          last_if_indent = ''
      continued = record.endswith('\\')
      line += 1
    error = (tab != 0)
    if(error):
      sys.stderr.write('File %s: error: indent/outdent mismatch: %d.\n' % (path,tab))
    return '\n'.join(output), error

  def beautify_file(self,path):
    error = False
    if(path == '-'):
      data = sys.stdin.read()
      result,error = self.beautify_string(data,'(stdin)')
      sys.stdout.write(result)
    else: # named file
      data = self.read_file(path)
      result,error = self.beautify_string(data,path)
      if(data != result) and self.do_backup:
        # make a backup copy
        self.write_file(path + '~',data)
        self.write_file(path,result)
    return error

  def main(self,args):
    self.tab_str = args.tab_str
    self.tab_size = args.tab_size
    self.do_backup = not args.no_backup
    error = False
    if(len(args.files) < 1):
      sys.stderr.write('usage: shell script filenames or \"-\" for stdin.\n')
    else:
      for path in args.files:
        error |= self.beautify_file(path)
    sys.exit((0,1)[error])

# CLI entry point
def main():
    parser = argparse.ArgumentParser(description='Bash Script Beautifier.')

    parser.add_argument('--tab-str', '-c', metavar='CHAR',
                        help='Tab string (default: " ")', default=' ')
    parser.add_argument('--tab-size', '-t', metavar='TAB', type=int,
                        help='Tab size (default: 2)', default=2)
    parser.add_argument('--no-backup', '-n', action='store_true',
                        help='Do not backup file before overwrite', default=False)
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='Filename (use "-" for stdin)')

    args = parser.parse_args()

    BeautifyBash().main(args)

# if not called as a module
if(__name__ == '__main__'):
  main()
