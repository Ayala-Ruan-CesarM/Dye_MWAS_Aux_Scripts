#!/bin/bash
# Desde la linea 3 a la 35 permite ejecutar el script desde la terminal
  if [ "$1" = "-?" ] || [ "$1" = "-h" ] || [ $# -le 1 ]                                                     #
  then                                                                                                      #
    cat << EOF                                                       


 USAGE:  script_split_hic.sh  -i <file>  -o <namefile>  

 OPTIONS:

    -i <input>      Input secuence file (mandatory)
    -o <output>     Output name adding the .fasta extesion (mandatory)

EOF
    if [ "$1" = "-?" ] || [ "$1" = "-h" ] || [ $# -le 0 ]; then exit 0 ; fi                                 #
    exit 1 ;                                                                                                #
  fi                                                                                                        #
#                                                                                                           #

export LC_ALL=C ;

INPUT="N.O_L.I.S.T";       # -i (mandatory)
OUTPUT="N.O_O.U.T";        # -o (mandatory)

while getopts :i:o:nfx option
do
  case $option in
    i) INPUT="$OPTARG"                                                            ;;
    o) OUTPUT="$OPTARG"                                                           ;;
  esac
done

if [ "$INPUT" == "N.O_L.I.S.T" ]; then echo "file is not specified (option -i)"       >&2 ; exit 1 ; fi
if [ "$OUTPUT" == "N.O_O.U.T" ];  then echo "basename is not specified (option -o)"               >&2 ; exit 1 ; fi
## Es posible modificar la secuencia quimerica así como el numero de 
## sitios
site1=GATCGATC
site2=AATTAATT
site3=GATCAATT
## sed elimina la unión quimerica, introduce un salto de linea
## como una nueva secuencia
sed -e "s/"$site1"/\n>Seq1\n/g" -e "s/"$site2"/\n>Seq2\n/g" -e "s/"$site3"/\n>Seq3\n/g" "$INPUT" > tmp_file
sleep 5
## awk permite reformatear el nombre y numero de las secuencias
awk '/>.*/{sub(/[^;]*/,">Sequence_" ++i )}1' tmp_file > $OUTPUT
rm tmp_file