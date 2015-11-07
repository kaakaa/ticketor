%rebase layout page='burndown'

<div class="jumbotron">
  <div class="container">
    <h1>Burndown</h1>
    <p>バーンダウンチャート</p>
    <form role="form" data-toggle="validator" action="/burndown" method="post">
      <div class="row">
        <div class="form-group col-md-6">
          <label for="milestone">マイルストーン: </label>
          <select class="form-control" name="milestone" id="milestone" required>
            <option></option>
            %for ms in get_milestones():
              <option>{{ms}}</option>
            %end
          </select>
        </div>
        <div class="form-group col-md-6">
          <label for="milestone">ユーザー: </label>
          <select class="form-control" name="member" id="member" required>
            <option></option>
            <option>ALL</option>
            %for m in get_team_members():
              <option>{{m}}</option>
            %end
          </select>
        </div>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary">View</button>
      </div>
    </form>
  </div>
  
  <hr>
  
  <div class="container">

    %if len(data) > 0:
      <script src="/js/ccchart.js" charset="utf-8"></script>
      <canvas id="chart"></canvas>
      <button type="button" id="downloadchart" class="btn btn-primary">Save</button>      
      <script>
        var chartdata2 = {
          "config": {
            "title": "Burndown Chart - {{member}}",
            "subTitle": "ccchartを使ったバーンダウンチャート",
            "bg": "white",
            "textColor": "black",
            "useShadow": "no",
            "type": "line",
            "lineWidth": 4,
            "useMarker": "css-ring",
            "markerWidth": 12,
            "colorSet": ["rgba(255,0,128,0.3)","red","#3CB000","#00A8A2","#0036C0","#C328FF","#FF34C0"],
            "useVal": "yes",
            "valFont": ["100 18px 'Arial'","100 18px 'Arial'"],
            "valYOffset": [30, -30],
            "unit": "Point",
            "width": 1080,
            "height": 640,
            "paddingTop": 150
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
    %end
  </div>
</div>
