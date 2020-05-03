SCRIPT_PATH=`realpath $0`
SCRIPT_FOLDER=`dirname $SCRIPT_PATH`
cd $SCRIPT_FOLDER/../lighthouse-reports

while read line; do
	echo $line
	/usr/local/bin/lighthouse --output json --output html --chrome-flags="--headless" $line
done < $SCRIPT_FOLDER/../list.txt
