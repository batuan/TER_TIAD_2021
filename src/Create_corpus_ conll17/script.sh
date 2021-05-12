soure_file=`ls *.tar`
lang=`ls *.tar | head -1 | cut -d "-"  -f1`
yourfilenames1=`tar -tf $soure_file | grep "wikipedia-" | head -9`
yourfilenames2=`tar -tf $soure_file | grep "common_crawl-" | head -9`
for eachfile in $yourfilenames1
do
   tar --extract --file=$soure_file $eachfile 	
   unxz $eachfile
   short_file="$(echo $eachfile | cut -d. -f1-2 )"
   cat $short_file | python3 process.py >> merge.txt
   rm  -rf $lang
done

for eachfile in $yourfilenames2
do
   tar --extract --file=$soure_file $eachfile 	
   unxz $eachfile
   short_file="$(echo $eachfile | cut -d. -f1-2 )"
   cat $short_file | python3 process.py >> merge.txt
   rm  -rf $lang
done