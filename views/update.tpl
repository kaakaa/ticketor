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
          <label for="member">Member: </label>
          <select class="form-control" name="member" id="member">
            %for member in members:
              <option>{{member}}</option>
            %end
          </select>
        </div>        
      </div>
      <div class="row">
        <div class="form-group col-md-4">
          <label for="component">Component: </label>
          <select class="form-control" name="component" id="component">
            %for ms in components:
              <option>{{ms}}</option>
            %end
          </select>
        </div>
        <div class="form-group col-md-4">
          <label for="milestone">Milestone: </label>
          <select class="form-control" name="milestone" id="milestone">
            %for ms in milestones:
              <option>{{ms}}</option>
            %end
          </select>
        </div>
      </div>
      <div class="row">
        <div class="form-group col-md-4">
          <label for="title">Due Assign:</label>
          <input type="text" class="form-control" name="due_assign" id="due_assign">
        </div>
        <div class="form-group col-md-4">
          <label for="title">Due Close:</label>
          <input type="text" class="form-control" name="due_close" id="due_close">
        </div>
      </div>
      <button type="submit" class="btn btn-default">Submit</button>
    </form>
  </div>
  
  <hr>
  
  <div class="container">
    <h2>Tickets</h2>
    <form role="form" action="/update" method="post">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Reporter</th>
            <th>Due Assigin</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          %for ticket in tickets:
            <tr>
              <td><label><input type="checkbox" name="ticketid" value="{{ticket['id']}}">{{ticket['id']}}</input></label></td>
              <td>{{ticket['summary']}}</td>
              <td>{{ticket['reporter']}}</td>
              <td>{{ticket['due_assign']}}</td>
              <td>{{ticket['status']}}</td>
            </tr>
          %end
        </tbody>
      </table>
      
      <hr>
      
      <p><b>Change Status</b></p>
      <p>
        <label class="radio-inline"><input type="radio" value="new" name="status" id="status">new</label>
        <label class="radio-inline"><input type="radio" value="assigned" name="status" id="status">assigned</label>
        <label class="radio-inline"><input type="radio" value="accepted" name="status" id="status">accepted</label>
        <label class="radio-inline"><input type="radio" value="closed" name="status" id="status">closed</label>
      </p>
      <div class="row">
        <div class="form-group col-md-4">
          <label for="member">Member(acceptedを選択した場合は必須): </label>
          <select class="form-control" name="targetuser" id="targetuser">
            %for member in members:
              <option>{{member}}</option>
            %end
          </select>
        </div>
      </div>
      <button type="submit" class="btn btn-default">Update</button>
    </form>
  </div>
</div>

