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
            <li id='nav-form'><a href="/form">Regist Team Task</a></li>
            <li id='nav-tasks'><a href="/tasks">Team Tasks</a></li>
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
        </div><!--/.nav-collapse -->
      </div><!--/.container-fluid -->
    </nav>
    
    %include
    
  </div>
  <script type="text/javascript" src="/js/jquery-1.11.3.min.js"></script>
  <script type="text/javascript" src="/js/bootstrap.min.js"></script>
  <script type="text/javascript">
    $(function(){
      $('#desc').val('== 概要 == \r\n\r\n\r\n== 前提条件 == \r\n\r\n\r\n== 完了条件 ==');
	  $('#nav-{{page}}').addClass('active');
    });
  </script>
</body>
</html>
