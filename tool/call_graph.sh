#!/bin/sh
set -eu

#####################################################################
# help
#####################################################################

print_usage_and_exit () {
  cat <<-USAGE 1>&2
Usage   : ${0##*/} <call relation file>
Options : -o<output name>

Visualize the call relations.

-o: Specify the output file name (default: input file name + .png)
USAGE
  exit 1
}

#####################################################################
# paramter
#####################################################################

opr=''
opt_o=''

i=1
for arg in ${1+"$@"}
do
  case "${arg}" in
    -h|--help|--version) print_usage_and_exit ;;    
    -o*)                 opt_o="${arg#-o}"    ;;
    *)
      if [ $i -eq $# ] && [ -z "${opr}" ] ; then
        opr="${arg}"
      else
        echo "ERROR:${0##*/}: invalid args" 1>&2
        exit 1
      fi
      ;;
  esac

  i=$((i + 1))
done

if ! type dot >/dev/null 2>&1; then
  echo "ERROR:${0##*/}: dot command not found" 1>&2
  exit 1
fi

if   [ "${opr}" = '' ] || [ "${opr}" = '-' ]; then
  opr='-'
elif [ ! -f "${opr}" ] || [ ! -r "${opr}"  ]; then
  echo "${0##*/}: invalid file specified <${opr}>" 1>&2
  exit 1
else
  :
fi

REL_FILE="${opr}"

if [ -n "${opt_o}" ]; then
  OUT_FILE="${opt_o%.png}.png"
else
  if [ "${opr}" = '-' ]; then
    OUT_FILE="stdin_$(date '+%Y%m%d_%H%M%S').png"
  else
    OUT_FILE="${opr%.png}.png"
  fi
fi

#####################################################################
# main routine
#####################################################################

cat "${REL_FILE}"                                                   |

awk '
{
  caller = $1;
  callee = $2;
  field_num = NF;
  line_num  = NR;

  if (field_num != 2) {
    print "WARN:'"${0##*/}"': invalid line at <" line_num ">"       \
      > "/dev/stderr";
  }
  else {
    print caller, callee
  }
}
'                                                                   |

sort                                                                |
uniq                                                                |

awk '{ print $1, "->", $2; }'                                       |
sed 's/$/;/'                                                        |

{ 
  cat <<'  EOF'
  digraph graph_name {
    graph [
      charset = "UTF-8";
      layout  = dot;
    ];
  EOF

  cat
  
  cat <<'  EOF'
  }
  EOF
}                                                                   |

dot -Tpng >"${OUT_FILE}"
