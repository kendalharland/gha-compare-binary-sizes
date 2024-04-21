#!/usr/bin/python3

import pandas as pd
import argparse
import math

SIZE_INCREASED_COLOR = 'red'
SIZE_DECREASED_COLOR = 'lime'
SIZE_UNCHANGED_COLOR = 'gray'

SIZE_INCREASED_SYMBOL = '▲'
SIZE_DECREASED_SYMBOL = '▼'
SIZE_UNCHANGED_SYMBOL = ' '

def format_rounded_number(number):
  power = 0
  while number > 1000 and power < 4:
     power += 1
     number /= 1000
  
  units = {
     0: 'B',
     1: 'KB',
     2: 'MB',
     3: 'GB',
     4: 'B',
  }[power]

  return f"{number }"

def format_byte_difference_as_markdown_table_cell(value):
  if value > 0:
      color = SIZE_INCREASED_COLOR
      symbol = SIZE_INCREASED_SYMBOL
  elif value < 0:
      color = SIZE_DECREASED_COLOR
      symbol = SIZE_DECREASED_SYMBOL
  else:
      color = SIZE_UNCHANGED_COLOR
      symbol = SIZE_UNCHANGED_SYMBOL

  value = math.fabs(value)

  power = 0
  while value > 1000 and power < 4:
    power += 1
    value /= 1000
  
  unit = {
    0: 'B',
    1: 'KB',
    2: 'MB',
    3: 'GB',
  }[power]  

  return f'$\color{{{color}}}{{\\textsf{{{value:.2f} {unit} {symbol}}}}}$'

def format_dataframe_as_markdown_table(df):
  table_data = [
    '| Filename | File Size Delta | VM Size Delta |',
    '| -:       | -:              | -:            |',
  ]

  for index, row in df.iterrows():
    filename = index
    col_filesize = format_byte_difference_as_markdown_table_cell(row['filesize'])
    col_vmsize = format_byte_difference_as_markdown_table_cell(row['vmsize'])
    table_data.append(f'|{filename}|{col_filesize}|{col_vmsize}|')

  return '\n'.join(table_data)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("old_output_file", help="Golden bloaty output to use as a baseline")
  parser.add_argument("new_output_file", help="Bloaty output for the current build")
  parser.add_argument("-o", "--output-path", help="Where to write the output")
  parser.add_argument("-f", "--output-format", help="How to format the output", type=str, choices=['markdown'], default='markdown')
  args = parser.parse_args()

  assert(len(args.output_path) > 0)
  
  old_df = pd.read_csv(args.old_output_file)
  new_df = pd.read_csv(args.new_output_file)

  # Compute size diffs.
  old_df = old_df.groupby(['inputfiles']).agg({'filesize':'sum', 'vmsize': 'sum'})
  new_df = new_df.groupby(['inputfiles']).agg({'filesize':'sum', 'vmsize': 'sum'})
  diff_df = new_df - old_df
  
  # Drop rows for deleted and newly added files. Their size values are NaN.
  diff_df.dropna(inplace=True)
  diff_df.reset_index()

  assert(args.output_format == 'markdown')

  output = format_dataframe_as_markdown_table(diff_df)

  with open(output_file, 'w+', encoding='utf-8') as output_file:
     output_file.write(output)

main()