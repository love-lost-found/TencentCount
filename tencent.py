import os
import threading
import requests
import re
import time

s1 = """
<html>
<head>
<meta charset="UTF-8" />
<title>腾讯视频播放量统计</title>
<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body>
<div id="container" style="width: 550px; height: 400px; margin: 0 auto"></div>
<script language="JavaScript">
$(document).ready(function() {  
   var chart = {
      zoomType: 'x'
   }; 
   var title = {
      text: '统计《且听凤鸣》在腾讯视频上的播放量'   
   };
   var subtitle = {
      text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' :
                    'Pinch the chart to zoom in'
   };
   var xAxis = {
      type: 'datetime',
      minRange: 3600000/12 // 14 天
   };
   var yAxis = {
      title: {
         text: '播放量'
      }
   };
   var legend = {
      enabled: false 
   };
   var plotOptions = {
      area: {
         fillColor: {
            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
            stops: [
               [0, Highcharts.getOptions().colors[0]],
               [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            ]
         },
         marker: {
            radius: 2
         },
         lineWidth: 1,
         states: {
            hover: {
               lineWidth: 1
            }
         },
         threshold: null
      }
   };
   var series= [{
      type: 'area',
      name: '播放量',
      pointInterval:  300 * 1000,
      pointStart: Date.UTC(2020, 8, 12,15,15),
      data: [
"""

s2 = """

         ]
      }
   ];
   
   var json = {};
   json.chart = chart;
   json.title = title;
   json.subtitle = subtitle;
   json.legend = legend;
   json.xAxis = xAxis;
   json.yAxis = yAxis;  
   json.series = series;
   json.plotOptions = plotOptions;
   $('#container').highcharts(json);
  
});
</script>
</body>
</html>

"""

re_num = re.compile('interactionCount\" content="(.+?)\"')
#定义函数
def get_num():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'cache-control': 'no-cache',
        #'cookie': 'tvfe_boss_uuid=f46c9616ebd4d932; pgv_pvid=8752282767; ts_refer=www.baidu.com/link; ts_uid=131770696; login_remember=wx; pgv_pvi=4741858304; video_guid=587a541c2170f07d; video_platform=2; pgv_info=ssid=s2758728144; bucket_id=9231005; ts_last=v.qq.com/x/cover/mzc00200d8fkodt.html; ptag=; ad_play_index=58',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
    url = 'https://v.qq.com/x/cover/mzc00200d8fkodt.html' 
    rt = requests.get(url,headers=headers)
    num = re_num.search(rt.text)
    return num.group(1)
    
       

def fun_timer():
    num = get_num()
    with open('data.text','a') as f:
        s = str(num)+','+str(time.time())+'\n'
        f.write(s)
        print(s)
    with open('data.text','r') as f:
        t = []
        for data in f.readlines():
            try:
                t.append(data.split(',')[0])
            except:
                print('error')
                pass
    
    ts = ','.join(t)
    with open('index.html','w') as f:
        temp = s1+ts+s2
        
        f.write(str(temp))
    os.system('git add .')
    os.system('git commit -m "upload"')
    os.system('git push -u origin master')
    time.sleep(300)
    fun_timer()
fun_timer()


