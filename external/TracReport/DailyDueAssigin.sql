SELECT Day as __group__,
       Day,
       ticket,
       summary,
       component,
       point,
       _ORD as __color__ 
from (
select  d.value as Day,
        t.id as ticket,
        t.summary as summary,
        t.component as component,
        p.value as point,
        0 as _ORD
 from (select * from ticket) t,
      (select * from ticket_custom where name = 'point') p,
      (select * from ticket_custom where name = 'due_assign') d
      where t.reporter = $MEMBER AND t.milestone = $MS AND t.id = p.ticket AND t.id = d.ticket
 group by Day,ticket

UNION

select d.value as Day,
       0   as ticket,
       '合計' as summary,
       '  ' as component,
       SUM(p.value) as point,
       5 as _ORD
 from (select * from ticket) t,
      (select * from ticket_custom where name = 'point') p,
      (select * from ticket_custom where name = 'due_assign') d
      where t.reporter = $MEMBER AND t.milestone = $MS AND t.id = p.ticket AND t.id = d.ticket
 group by Day
)
order by Day,_ord
