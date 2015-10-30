%rebase layout page='burndown'

<div class="jumbotron">
  <div class="container">
    <h1>Burndown</h1>
    <p>バーンダウンチャート  <button type="button" id="downloadchart" class="btn btn-primary">SAVE</button></p>
  </div
  
  <hr>
  
  <div class="container">
    <script src="http://ccchart.com/js/ccchart.js" charset="utf-8"></script>
    <canvas id="chart"></canvas>
    
    <script>
      var chartdata2 = {
        "config": {
          "title": "Burndown Chart",
          "subTitle": "ccchartを使ったバーンダウンチャート",
          "type": "line",
          "lineWidth": 4,
          "colorSet": ["red","#FF9114","#3CB000","#00A8A2","#0036C0","#C328FF","#FF34C0"],
          "bgGradient": {
            "direction":"vertical",
            "from":"#687478",
            "to":"#222222"
          },
          "useMarker": "css-ring",
          "markerWidth": 12,
          "width": 960,
          "height": 540
        },
    
        "data": [
          [
            "年度",
            "2015/11/2",
            "2015/11/3",
            "2015/11/4",
            "2015/11/5",
            "2015/11/6",
            "2015/11/9",
            "2015/11/10",
            "2015/11/11",
            "2015/11/12",
            "2015/11/13",
          ],
          ["紅茶",9,332,524,688,774,825,999,774,825,999],
          ["コーヒー",600,335,584,333,457,788,900,774,825,999],
          ["ジュース",60,435,456,352,567,678,1260,774,825,999],
          ["ぶどうジュース",60,435,456,352,567,678,1260,774,825,999],
          ["オレンジジュース",60,435,456,352,567,678,1260,774,825,999],
          ["りんごジュース",60,435,456,352,567,678,1260,774,825,999],
          ["ウーロン",200,123,312,200,402,300,512,774,825,999]
        ]
      };
      ccchart.init('chart', chartdata2)
    </script>
    <script type="text/javascript" src="/js/download.js"></script>
    <script type="text/javascript">
      $('#downloadchart').on('click', function(event) {
        event.preventDefault();
        var canvas = document.getElementById('chart');
        download(canvas.toDataURL('image/png'), 'burndown.png', 'image/png');
      });
    </script>
  </div>
</div>
