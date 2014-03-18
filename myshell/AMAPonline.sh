#!/bin/sh

if [ $# -eq 1 ];then
        yesday=$1
#$#添加到shell的参数个数
else	
	yesday=`date +%Y%m%d -d "1 days ago"`
fi
redisIp="127.0.0.1:20000"
root=/opt/data
IPADDR=`/sbin/ifconfig -a|grep "10.13"|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`

cd $root
mkdir -p $yesday

scpdata()
{	
for((times=1;times<4;times++))	
do
	cd  $root/$yesday
	echo "loop $times wget start:"`date +%Y%m%d' '%H':'%M':'%S` >>./$IPADDR-$yesday.txt
	wget -c "http://119.90.32.8:8080/download/locData.$yesday.tar.gz"
	wget -c "http://119.90.32.8:8080/download/locData.$yesday.md5"
	echo "wget end:"`date +%Y%m%d' '%H':'%M':'%S` >>./$IPADDR-$yesday.txt
	md5online=`md5sum     locData.$yesday.tar.gz|awk  '{print$1}'`
	md5offline=`cat  locData.$yesday.md5`
	if  [ $md5online == $md5offline ]; then times=4;echo "scp file complete">>./$IPADDR-$yesday.txt; fi
done
}

loaddata()
{	
cd  $root/$yesday
 
echo "tar start:"`date +%Y%m%d' '%H':'%M':'%S` >>./$IPADDR-$yesday.txt
tar -xzvf locData.$yesday.tar.gz
echo "tar end:"`date +%Y%m%d' '%H':'%M':'%S` >>./$IPADDR-$yesday.txt
java -jar /opt/LocationData2Mem.jar redis $redisIp $root/$yesday/  $yesday >> ./$IPADDR-$yesday.txt
#rm   -rf   ${yesday}* 
#cat   >>./$IPADDR-$yesday.txt
}


scpdata
if [ -f ${root}/$yesday/locData.$yesday.tar.gz ]; then 
     loaddata
     echo $yesday

     sh /opt/myshell/scplog.sh 
fi

