%rebase layout page='settings'

<div class="container-fluid">
  <div class="row">
    <div class="col-sm-3 col-md-2 sidebar">
      <ul class="nav nav-sidebar">
        <li class="active"><a href="#">Trac Server<span class="sr-only">(current)</span></a></li>
      </ul>
    </div>
    
    <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
      <h1 class="page-header">Trac Server</h1>

      <div class="row">
        <dl>
          <dt>Loading at:</dt>
          <dd>{{loading_at}}</dd>
        </dl>
      </div>

      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>HOST</td>
              <td>{{host}}</td>
            </tr>
            <tr>
              <td>PORT</td>
              <td>{{port}}</td>
            </tr>
            <tr>
              <td>ProjectName</td>
              <td>{{project_name}}</td>
            </tr>
            <tr>
              <td>Team Name</td>
              <td>{{team_name}}</td>
            </tr>
            <tr>
              <td>Team Members</td>
              <td>{{' / '.join(members)}}</td>
            </tr>
            <tr>
              <td>Milestones</td>
              <td>{{' / '.join(milestones)}}
            </tr>
            <tr>
              <td>TracRPC User</td>
              <td>{{auth.get('user')}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
      <form action="/servertest" method="post">
        <button type="button" id="servertest" class="btn btn-danger">Connection Test</button>
        <button type="button" id="reload" class="btn btn-primary">Reload</button>
      </form>
      <div class="alert alert-success fade" id="result" style="margin-top: 10px;">
        <a class="close" data-dismiss="alert" href="#">&times;</a>
        <p id="resultText">hge</p>
      </div>
    </div>
  </div>
</div>

<script type="text/javascript">
  $(function(){
    $("#servertest").click(function() {
      $.ajax({
        type: 'get',
        url: '/servertest',
        success: function(data){
          $('#resultText').text('Connection is success.');
          $('#result').removeClass('alert-danger');
          $('#result').addClass('alert-success');
          $('#result').addClass('in');
        },
        error: function(data){
          console.log(data);
          $('#resultText').text('Connection is failed. ' + data.status + ':' + data.responseText);
          $('#result').removeClass('alert-success');
          $('#result').addClass('alert-danger');
          $('#result').addClass('in');
        }
      });
    });
    $("#reload").click(function() {
      $.ajax({
        type: 'get',
        url: '/reload',
        success: function(data){
          // TODO partialy reload
          location.reload();
        },
        error: function(data){
          $('#resultText').text('Reload is failed...')
          $('#result').removeClass('alert-success');
          $('#result').addClass('alert-danger');
          $('#result').addClass('in');
        }
      });
    });
  });
</script>
