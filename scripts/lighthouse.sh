SCRIPT_PATH=`realpath $0`
SCRIPT_FOLDER=`dirname $SCRIPT_PATH`
cd $SCRIPT_FOLDER/../lighthouse-reports

INPUT=$SCRIPT_FOLDER/../list.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read url government etc
do
	/usr/local/bin/lighthouse --output json --output html --chrome-flags="--headless" $url
done < $INPUT
