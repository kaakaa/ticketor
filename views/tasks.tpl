%rebase layout page='tasks'

<div class="jumbotron team-tasks">
  <h1><a name="team-tasks">Archives</a></h1>
  <p>過去のタスク</p>
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
