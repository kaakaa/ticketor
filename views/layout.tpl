<!doctype html>
<html lang="ja">
<head>
  <title>TracTicketor</title>
  <link rel="stylesheet" href="/css/bootstrap.min.css">
  <link rel="stylesheet" href="/css/bootstrap-theme.min.css">
  <link rel="stylesheet" href="/css/jquery-ui.min.css">
  <link rel="stylesheet" href="/css/jquery-ui.structure.min.css">
  <link rel="stylesheet" href="/css/jquery-ui.theme.min.css">
  <script type="text/javascript" src="/js/jquery-1.11.3.min.js"></script>
  <script type="text/javascript" src="/js/jquery-ui.min.js"></script>
  <script type="text/javascript" src="/js/bootstrap.min.js"></script>
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
          <a class="navbar-brand" href="/">Trac Ticketor</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li id='nav-form'><a href="/form">Regist Team Task</a></li>
            <li id='nav-update'><a href="/update">Update Task</a></li>
            <li id='nav-burndown'><a href="/burndown">Burndown</a></li>
            <li id='nav-archives'><a href="/archives">Archives</a></li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Trac<span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="{{get_trac_home()}}">Top</a></li>
                <li><a href="{{get_kanban_home()}}">Kanban</a></li>
              </ul>
            </li>
          </ul>
        </div><!--/.nav-collapse -->
      </div><!--/.container-fluid -->
    </nav>
    
    %include

  </div>
  <script type="text/javascript">
    $(function(){
      $('#desc').val('== 目的 == \r\n\r\n\r\n== 前提条件 == \r\n\r\n\r\n== 完了条件 ==');
      $('#nav-{{page}}').addClass('active');
      
      $("#due_assign").datepicker({dateFormat: 'yy/mm/dd'});
      $("#due_close").datepicker({dateFormat: 'yy/mm/dd'});
    });
  </script>
</body>
</html>
