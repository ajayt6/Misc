#arguments: interface, time
INTF=$1
TIME=$2

rx=$(echo "scale=5; $(ifconfig ${INTF} | grep -v grep | grep bytes | awk '{print $2}' | cut -d ':' -f 2) / 1024.0 " | bc )

tx=$(echo "scale=5; $(ifconfig $INTF | grep -v grep | grep bytes | awk '{print $6}' | cut -d ':' -f 2) / 1024 " | bc )

sleep $2

rx2=$(echo "scale=5; $(ifconfig ${INTF} | grep -v grep | grep bytes | awk '{print $2}' | cut -d ':' -f 2) / 1024.0" | bc )

tx2=$(echo "scale=5; $(ifconfig $INTF | grep -v grep | grep bytes | awk '{print $6}' | cut -d ':' -f 2) / 1024" | bc )


rdiff=$(echo "scale=5; ($rx2-$rx)/$2" | bc)
tdiff=$(echo "scale=5; ($tx2-$tx)/$2" | bc)
#let tdiff=$tx2-$tx

echo $rdiff, $tdiff
