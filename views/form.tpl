<html>
<head>
  <title>hogehoge</title>
  <link rel="stylesheet" href="/css/bootstrap.min.css">
  <link rel="stylesheet" href="/css/bootstrap-theme.min.css">
</head>
<body>
  <div class="container">
    <!-- Static navbar -->
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Trac Ticktor</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#regist">Regist Team Task</a></li>
            <li><a href="#team-tasks">Team Tasks</a></li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="#">Action</a></li>
                <li><a href="#">Another Action</a></li>
                <li><a href="#">Something else here</a></li>
                <li role="separator" class="driver"></li>
                <li class="dropdown-header>Nav header</li>
                <li><a href="#">Separated link</a></li>
                <li><a href="#">One more separated link</a></li>
              </ul>
            </li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li class="active"><a href="./">Default <span class="sr-only">(current)</span></a></li>
            <li><a href="../navbar-static-top/">sStatic top</a></li>
            <li><a href="../navbar-fixed-top/">Fixed top</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div><!--/.container-fluid -->
    </nav>
    
    <div class="jumbotron">
      <h1><a name="regist">Regist Team Task</a></h1>
      <form role="form" action="/regist" method="post">
        <div class="row">
          <div class="form-group col-md-8">
            <label for="title">Title:</label>
            <input type="text" class="form-control" name="title" id="title">
          </div>
          <div class="form-group col-md-4">
            <label for="milestone">Milestone: </label>
            <select class="form-control" name="milestone" id="milestone">
              <option>Iterate1</option>
              <option>Iterate2</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="desc">Description:</label>
          <textarea class="form-control" rows="10" name="desc" id="desc"></textarea>
        </div>
        <div class="row">
          <div class="form-group col-md-4">
            <label for="point">Point: </label>
            <select class="form-control" name="point" id="point">
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>5</option>
              <option>8</option>
              <option>13</option>
            </select>
          </div>
          <div class="form-group col-md-4">
            <label for="title">Due Start:</label>
            <input type="text" class="form-control" name="due_start" id="due_start">
          </div>
          <div class="form-group col-md-4">
            <label for="title">Due Close:</label>
            <input type="text" class="form-control" name="due_close" id="due_close">
          </div>
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>
    </div>
    
    
    <div class="jumbotron team-tasks">
      <h1><a name="team-tasks">Team Tasks</a></h1>
      <p>チームタスク一覧</p>
    </div>
  </div>
  
  <script type="text/javascript" src="/js/jquery-1.11.3.min.js"></script>
  <script type="text/javascript" src="/js/bootstrap.min.js"></script>
  <script type="text/javascript">
    $(function(){
      $('#desc').val('== 概要 == \r\n\r\n\r\n== 前提条件 == \r\n\r\n\r\n== 完了条件 ==');
    });
  </script>
</body>
</html>
