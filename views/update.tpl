%rebase layout page='update'

<div class="jumbotron">
  <div class="container">
    <h1>Update Task</h1>
    <p>タスクの状態を一括で更新する</p>
  </div>
  
  <hr>
  
  <div class="container">
    <h2>Query</h2>
    <form role="form" action="/search" method="post">
      <div class="row">
        <div class="form-group col-md-4">
          <label for="member">報告者: </label>
          <select class="form-control" name="member" id="member">
            <option></option>
            %for member in get_team_members():
              <option>{{member}}</option>
            %end
          </select>
        </div>
        <div class="form-group col-md-4">
          <label for="owner">担当者: </label>
          <select class="form-control" name="owner" id="owner">
            <option></option>
            %for member in get_team_members():
              <option>{{member}}</option>
            %end
          </select>
        </div>
      </div>
      <div class="row">
        <div class="form-group col-md-4">
          <label for="component">コンポーネント: </label>
          <select class="form-control" name="component" id="component">
            <option></option>
            %for ms in get_components():
              <option>{{ms}}</option>
            %end
          </select>
        </div>
        <div class="form-group col-md-4">
          <label for="milestone">マイルストーン: </label>
          <select class="form-control" name="milestone" id="milestone">
            <option></option>
            %for ms in get_milestones():
              <option>{{ms}}</option>
            %end
          </select>
        </div>
      </div>
      <div class="row">
        <div class="form-group col-md-4">
          <label for="title">開始予定日:</label>
          <input type="text" class="form-control" name="due_assign" id="due_assign">
        </div>
        <div class="form-group col-md-4">
          <label for="title">終了予定日:</label>
          <input type="text" class="form-control" name="due_close" id="due_close">
        </div>
      </div>
      <button type="submit" class="btn btn-default">検索</button>
    </form>
  </div>
  
  <hr>
  
  <div class="container">
    %if len(tickets) != 0:
      <form role="form" action="/update" method="post" data-toggle="validator">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>タイトル</th>
              <th>報告者</th>
              <th>開始予定日</th>
              <th>状態</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><label><input type="checkbox" data-toggle="popover" data-placement="top" data-content="最低１つはチェックしてください。" id="checkall" name="checkall">CheckAll</input></label></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
          </tbody>
          <tbody>
            %for ticket in tickets:
              <tr>
                <td><label>
                %if ticket.has_key('id'):
                  <input type="checkbox" class="check_id" name="ticketid" value="{{ticket['id']}}">{{ticket['id']}}</input>
                %end
                </label></td>
                <td>{{ticket.get('summary', '-')}}</td>
                <td>{{ticket.get('reporter','-')}}</td>
                <td>{{ticket.get('due_assign', '-')}}</td>
                <td>{{ticket.get('status', '-')}}</td>
              </tr>
            %end
          </tbody>
        </table>
        
        <hr>
        
        <h2>Change Status</h2>
        <div class="row">
          <div class="form-group col-md-4">
            <label for="member">Member</label>
            <select class="form-control" name="targetuser" id="targetuser" required>
              <option></option>
              %for member in get_team_members():
              <option>{{member}}</option>
              %end
            </select>
          </div>
        </div>
        <div class="form-group">
          <p>
            <label class="radio-inline"><input type="radio" value="new" name="status" id="status" checked>new</label>
            <label class="radio-inline"><input type="radio" value="assigned" name="status" id="status">assigned</label>
            <label class="radio-inline"><input type="radio" value="accepted" name="status" id="status">accepted</label>
            <label class="radio-inline"><input type="radio" value="closed" name="status" id="status">closed</label>
          </p>
        </div>
        <div>
          <button type="submit" id="update" class="btn btn-default">Update</button>
        </div>
        
        <div class="alert alert-danger fade" id="checkAtLeastOne" style="margin-top: 10px;">
          <a class="close" data-dismiss="alert" href="#">&times;</a>
          <p>更新するチケットを選択してください</p>
        </div>
      </form>
    %end
  </div>
</div>
<script type="text/javascript">
  $(function(){
    $("#update").click(function() {
      checked = $("input[type=checkbox]:checked").length;
      if(!checked) {
        $('#checkAtLeastOne').addClass('in');
        return false;
      }
    });
  });
  
  $("#checkall").click(function() {
    $(".check_id").prop('checked', $(this).prop('checked'));
  });
</script>
