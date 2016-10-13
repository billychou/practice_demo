#-*-coding:utf-8-*-
#!/usr/bin/env python

from selenium import webdriver
import requests 
import json

#是否支持GET
interface_list = {
	#取图服务
	"static_map":"/ws/mapapi/map/slice/?channel=autonavi&sign=55E9006437E8282E6824D416EB955911&mapscroll=&bmptype=png&bounds=116.384,39.98016,116.3878,39.98242&centx=116.38589999999999&centy=39.98129&poi=116.384,39.9823,amap_80,a,%E5%AE%8B%E4%BD%93,1,20,0xff0cc0,0xffffe0,1|116.3877,39.98242,25,b,%E5%AE%8B%E4%BD%93,1,20,0xff0cc0,0xffffe0,1|116.3878,39.98016,25,c,%E5%AE%8B%E4%BD%93,1,20,0xff0cc0,0xffffe0,1|116.3877,39.98018,25,d,%E5%AE%8B%E4%BD%93,1,20,0xff0cc0,0xffffe0,1&output=xml",
	"offline_map":"/ws/mapapi/map/packages/?category=1&maptype=3&admincode=340100&channel=autonavi&sign=E2AA5801E737573CDF1E28EBD5CA734C&output=json",
	"offline_map_best":"/ws/mapapi/map/offline/query/?channel=autonavi&map_ver=v4&poi_ver=v4&route_ver=v4&data_ver=%5B%7B%22adcode%22%3A+%22000000%22%2C%22map%22%3A+%2220140110%22%2C%22poi%22%3A+%2220140110%22%2C%22route%22%3A+%2220140110%22+%7D%2C%7B%22adcode%22%3A%22110000%22%2C%22map%22%3A+%2220140120%22%2C%22route%22%3A+%2220140115%22%2C%22poi%22%3A+%2220140122%22+%7D%2C%7B%22adcode%22%3A+%22440100%22%2C%22map%22%3A+%2220140120%22%2C%22route%22%3A+%2220140115%22%2C%22poi%22%3A+%2220140120%22%7D%5D&sign=14C413892D5720F83EFA9754ACE8DBA5",
	"offline_map_citylist": "/ws/mapapi/map/offline/district/?channel=autonavi&map_ver=v4&poi_ver=v4&route_ver=v4&sign=65AB99091A97C356140BE0AE9B8430B0",
	"intersection_maps": "/ws/mapapi/intersection/list/?flag=0&channel=amap&sign=809CF7909D55461D34B490886C7DA27B&output=json",
	"file_config": "/ws/mapapi/map/file-config?channel=autonavi&sign=F8BEE4456E609E604CA78779CD77FD71&id=1&output=json",
	#"subway_map": "/ws/mapapi/navigation/subway/conf/",
	#POI搜索
	"basic_info_search_poi": "/ws/mapapi/poi/info/?qii=true&hotelcheckin=2015-08-04+00%3A00%3A00&sign=5DEBC72CDE6719144B0C533B9D8AE155&query_acs=false&user_loc=119.45581555366518%2C32.2014207127773&pagenum=1&sort_rule=0&id=&category=10&city=0511&client_network_class=4&geoobj=&aosbusiness=nearbyhotel&version=2.13&hotelcheckout=2015-08-05+00%3A00%3A00&tid=UtFC6u0eaXkDAMih5PEtPnOr&channel=amap7&search_sceneid=312&addr_poi_merge=false&with_deepinfo=1&data_type=POI&query_type=RQBXY&cmspoi=1&appstartid=144810926&latitude=32.2014207127773&is_classify=true&cifa=manufacture=Meizu;SDKVersion=19;amapVersion=;bid=0;mcc=460;nid=0;height=1920;ant=1;device=m1note;entryTime=0;lac=21189;lat=32203347;mnc=0;wifimac=;strength=0;pt=1;cid=88849668;exitTime=0;lon=119450431;glrender=;width=1080;quiet_check=False;sid=0;model=m1 note;nt=13;accuracy=100&diu2=27f523e543c7ffffffe8&diu3=27e0a28a1a0842f793c6f6a7026f9a44-22bcb795cefaef741cc9e357b6793fcb&diu=866962020089342&stepid=69&pagesize=10&hotelissupper=false&longitude=119.45582360029222&dic=C8058&session=144810926&dibv=2217&search_operate=2&output=json&div=ANDH070201&dip=10880&spm=054825454447&re_poiid=B01FF02E9E%2CB01FF0P0FK%2CB01FF01OMF%2CB0FFFIR2L7%2CB01FF01R8E%2CB0FFG2SFMG%2CB01FF0O27W%2CB01FF009EA%2CB01FF01RHS%2CB01FF0PQKJ&request_serial_number=15a94401b07b42ec9a719e0c4323577d&business_brand=&re_querytype=5", 
	"basic_info_search_simple": "/ws/mapapi/poi/infolite/?pagenum=1&cluster_state=5&specialpoi=0&sign=FE6A98379B9685CD01CE8C65BC29CA9E&query_acs=false&need_codepoint=true&spm=2291781328224537367412781011984655442505511566&keywords=%E5%AE%BE%E9%A6%86&qii=true&log_center_id=&sort_rule=0&direct_jump=true&superid=a&need_recommend=1&search_operate=2&client_network_class=4&transfer_nearby_bucket=normal&version=2.17&need_utd=true&cmspoi=1&tid=VYo7Reu4E40BADXy0XR%2F2KOS&channel=amap7a&dibv=2028&data_type=POI&loc_strict=false&query_type=RQBXY&addr_poi_merge=true&appstartid=144814185&user_city=442000&latitude=22.58584112189023&is_classify=true&cifa=manufacture=Meizu;SDKVersion=19;amapVersion=;bid=0;mcc=460;nid=0;height=1280;ant=1;device=m1;entryTime=0;lac=9708;lat=22588683;mnc=0;wifimac=;strength=0;pt=1;cid=178754819;exitTime=0;lon=113210835;glrender=;width=768;quiet_check=False;sid=0;model=m1;nt=13;accuracy=100&diu2=fbcca0e543c7ffffffe8&diu3=25fa96c3bd9646b1855faa210771b2ab-7c79f884d1b80db790ae101880603582&need_parkinfo=true&transfer_nearby_keyindex=11&stepid=69&scenario=1&pagesize=10&transfer_nearby_time_opt=&citysuggestion=true&utd_sceneid=101000&longitude=113.21614444255829&dic=C8058&user_loc=113.21615248918533%2C22.58585721912247&session=144814185&need_magicbox=true&diu=866818023375924&output=json&div=ANDH070306&dip=10880&transfer_filter_flag=0&re_poiid=B0FFFFY2S6%2CB0FFF6ZNKN%2CB0FFG39GUW%2CB0FFFYQQIB%2CB0FFG11J7K%2CB02F80ORYL%2CB02F80Q1YN%2CB0FFFYHPN7%2CB0FFG39GV8%2CB0FFFORLPE&request_serial_number=f85d1daf6f1e48c1af691e775c76912f&business_brand=&re_querytype=5",

	#交通信息
	#"radar": "/ws/transfer/traffic/radar/?
}

status=0

print "===Interface_GET_list==="
for key,value in interface_list.items():
	driver = requests.get("http://m5.amap.com%s"%(value))
	result = driver.json()["result"]
	if result == "true":
		status=1
		print "%s--Success,status=%s"%(key,status)
	else:
		status=0
		print "%s--Failed--%s,status=%s"%(key,value,status)


payload={
	"frontcoords": "H4sIAAAAAAAAAzXJxw3AMAwEsIUOhk5dyP57pdj5kryotlx7SuBcybIqFAhtwcmUPz0GjYGJ7qSO65cqFomHwdlp7UO%2BGZ4WelJuVfGGGHUAAAA%3D",
	"offset": 1,
	"pincode": "AN_Amap_ADR_FC_ef3a2ca8-2352-4956-905b-f66117369b79",
	"session": "144812968&spm=236071831006863068741822667464531243137634025928",
	"cmdtype": "trafficinfo",
	"client_network_class": 2,
	"sdk_version": "3.5.1.1.1.20150718.6935.831",
	"gpsdata": "WfISXgpquYrBMByLRz5JAom6xwZtJsSm%2F1IE%2B8er%2F7cI9skEACYN8crMAMwR7M75AT0W582QA4Ya4tGPBaoe3dHyB5Ai2NNtClcm09LoDBoqztRxD%2FstydU%3D",
	"tid": "VLS8WtHwooMDAPJ4EhUPSMic",
	"channel": "amap7a",
	"t": "traffic",
	"compress": 1,
	"appstartid": 144812968, 
	"flag": 66847,
	"cifa": "manufacture=Meizu;SDKVersion=22;amapVersion=;bid=0;mcc=460;nid=0;height=1920;ant=0;device=m2note;entryTime=0;lac=49412;lat=41615021;mnc=1;wifimac=;strength=0;pt=1;cid=67315743;exitTime=0;lon=123422715;glrender=;width=1080;quiet_check=False;sid=0;model=m2 note;nt=3;accuracy=24",
	"diu2": "a62dfbcbc197ffffffe8",
	"diu3": "0a3f242f958b45c087431fa9d829f3f9-6b773b57a4672f90b87d77b358246625",
	"stepid": 235,
	"datatype": 1,
	"xiangying": "json",
	"dic": "C8058",
	"dibv": 2028,
	"diu": 867569028348841,
	"div": "ANDH070306", 
	"dip":10880,
	"empty": "",
	"request_serial_number":"28158a218c8d47ff83f6496ab66ecd89"
}

radar_p = requests.post("http://m5.amap.com/ws/transfer/traffic/radar/", data=payload)
print radar_p.text


