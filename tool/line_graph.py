#!/usr/bin/env python3

######################################################################
# default library
######################################################################

import os
import sys
import argparse
import datetime

#####################################################################
# utility
#####################################################################

def output_error(msg):
  print('ERROR:' + os.path.basename(__file__) + ': ' + msg, file=sys.stderr)

def output_info(msg):
  print('INFO:' + os.path.basename(__file__) + ': ' + msg, file=sys.stderr)

#####################################################################
# parameter
#####################################################################

parser = argparse.ArgumentParser()
parser.add_argument('input_file', nargs='?', type=str, default='-')
parser.add_argument('-d', '--output-dir', type=str, default='.')
parser.add_argument('-t', '--is-header', action='store_true')
parser.add_argument('--y-lower', type=int)
parser.add_argument('--y-upper', type=int)
parser.add_argument('--x-label', type=str, default='')
parser.add_argument('--y-label', type=str, default='')

args      = parser.parse_args()
in_file   = args.input_file
out_dir   = args.output_dir
is_header = args.is_header
y_lower   = args.y_lower
y_upper   = args.y_upper
x_label   = args.x_label
y_label   = args.y_label

if in_file == '-':
  in_file = sys.stdin
  is_stdin = True
elif os.access(in_file, os.F_OK):
  is_stdin = False
else:
  output_error('invalid file specified <' + in_file + '>')
  sys.exit(1)

if out_dir == '':
  output_error('output direcotry must be specified')
  sys.exit(1)
elif os.access(out_dir, os.W_OK):
  pass
else:
  output_info(out_dir + ' is newly made')
  os.makedirs(out_dir)

is_y_lower = (y_lower != None)
is_y_upper = (y_upper != None)

is_x_label = (x_label != "")
is_y_label = (y_label != "")

if is_stdin:
  prefix = 'stdin_'
else:
  prefix = os.path.basename(in_file) + '_'

date_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

out_name = prefix + date_now + '.png'
out_file = out_dir + '/' + out_name

#####################################################################
# external library
#####################################################################

try:
  import numpy as np
except ImportError:
  output_error('numpy not found')
  sys.exit(1)

try:
  import matplotlib.pyplot as plt
except ImportError:
  output_error('numpy not found')
  sys.exit(1)

#####################################################################
# prepare
#####################################################################

# input all data
if is_stdin:
  str_lines = sys.stdin.readlines()
else:
  with open(in_file, 'r') as f:
    str_lines = f.readlines()

if is_header:
  header = str_lines.pop(0).split()

#####################################################################
# main routine
#####################################################################
    
# interpret input as number
num_lines = []
for str_line in str_lines:
  num_lines.append([float(i) for i in str_line.split()])

# generate sequences of data
data_seq  = np.array(num_lines).transpose()
data_size = len(num_lines)

# generate a sequence of x-axis (one-origin)
axis_seq = np.array(range(data_size)) + 1

for i in range(data_seq.shape[0]):
  if is_header:
    plt.plot(axis_seq, data_seq[i], label=header[i])
  else:
    plt.plot(axis_seq, data_seq[i])

if is_header:
  plt.legend(loc = "upper left")

if is_y_lower:
  plt.ylim(bottom=y_lower)

if is_y_upper:
  plt.ylim(top=y_upper)

if is_x_label:
  plt.xlabel(x_label)

if is_y_label:
  plt.ylabel(y_label)

#####################################################################
# post
#####################################################################

plt.savefig(out_file)

print(out_name)
