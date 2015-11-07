%rebase layout page='form'

<div class="jumbotron">
  <div class="container">
    <h1>Regist Team Task</h1>
    <p>チームメンバー全員に向けたタスクの登録<br>
       ({{('/').join(get_team_members())}})</p>
  </div>
  
  <hr>
  
  <div class="container">
    <form role="form" data-toggle="validator" action="/regist" method="post">
      <div class="row">
        <div class="form-group col-md-8">
          <label for="title">タイトル:</label>
          <input type="text" class="form-control" name="title" id="title" required>
        </div>
      </div>
      <div class="form-group">
        <label for="desc">概要:</label>
        <textarea class="form-control" rows="10" name="desc" id="desc"></textarea>
      </div>
      <div class="row">
        <div class="form-group col-md-4">
          <label for="component">コンポーネント: </label>
          <select class="form-control" name="component" id="component">
            %for ms in get_components():
              <option>{{ms}}</option>
            %end
          </select>
        </div>
        <div class="form-group col-md-4">
          <label for="milestone">マイルストーン: </label>
          <select class="form-control" name="milestone" id="milestone">
            %for ms in get_milestones():
              <option>{{ms}}</option>
            %end
          </select>
        </div>
        <div class="form-group col-md-2">
          <label for="point">ポイント: </label>
          <select class="form-control" name="point" id="point">
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>5</option>
            <option>8</option>
            <option>13</option>
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
      <button type="submit" class="btn btn-default">Submit</button>
    </form>
  </div>
</div>

