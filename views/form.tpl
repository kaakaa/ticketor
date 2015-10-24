%rebase layout page='form'

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
