SELECT
       Day as __group__,
       Day,
       ticket,
       summary,
       component,
       point,
       _ORD as __color__ 
from (
select  c.author as author,
        date(c.time/1000000, 'unixepoch', 'localtime') as Day,
        c.ticket as ticket,
        t.summary as summary,
        t.component as component,
        p.value as point,
        0 as _ORD
 from (select * from ticket) t,
      (select * from ticket_custom where name = 'point') p,
      (select * from ticket_change where field = 'status' and newvalue = 'closed' AND author = $MEMBER) c
      where t.milestone = $MS AND t.id = p.ticket AND t.id = c.ticket
 group by Day,ticket

UNION

select author as author,
       date(c.time/1000000, 'unixepoch', 'localtime') as Day,
       0   as ticket,
       '合計' as summary,
       '  ' as component,
       SUM(p.value) as point,
       5 as _ORD
 from (select * from ticket) t,
      (select * from ticket_custom where name = 'point') p,
      (select * from ticket_change where field = 'status' and newvalue = 'closed' AND author = $MEMBER) c
      where t.milestone = $MS AND t.id = p.ticket AND t.id = c.ticket
 group by Day
)
order by Day,_ord
