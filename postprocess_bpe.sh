infile=$1
outfile=$2

sed -r 's/(@@ )|(@@ ?$)//g' < $infile > $outfile