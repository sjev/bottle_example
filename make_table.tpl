%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The open items are as follows:</p>
<table border="1">
<tr>
<th>id</th><th>task</th><th>open</th>
</tr>
%for row in rows:
  <tr>
      <td><a href="/edit/{{row[0]}}">{{row[0]}}</a></td>
      <td>{{row[1]}}</td>
      <td>{{row[2]}}</td>
  </tr>
%end
</table>