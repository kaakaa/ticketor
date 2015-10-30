%rebase layout page='burndown'

<div class="jumbotron">
  <div class="container">
    <h1>Burndown</h1>
    <p>バーンダウンチャート  <button type="button" id="downloadchart" class="btn btn-primary">SAVE</button></p>
  </div
  
  <hr>
  
  <div class="container">
    <script src="/js/ccchart.js" charset="utf-8"></script>
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
    
        "data": {{!data}}
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
