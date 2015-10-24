%rebase layout page='archives'

<div class="jumbotron">
  <div class="container">
    <h1>Archives</h1>
    <p>過去に登録したタスク</p>
  </div
  
  <hr>
  
  <div class="container">
    <table class="table table-hover">
      <thead>
        <tr>
          <th>Date</th>
          <th>Title</th>
          <th>Link</th>
        </tr>
      </thead>
      <tbody>
        %for archive in archives:
          <tr>
            <td>{{archive['Date']}}</td>
            <td>{{archive['Title']}}</td>
            <td><a href="{{archive['Link']}}">{{archive['Link']}}</a></td>
          </tr>
        %end
      </tbody>
    </table>
  </div>
</div>
