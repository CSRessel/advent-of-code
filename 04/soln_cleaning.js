var assignments = input.split("\n");
var assignmentIntervals = assignments.map(a => a.split(","));
var count = 0;
function intervalContains(a, b, x, y) {
  const ap = parseInt(a); const bp = parseInt(b); const xp = parseInt(x); const yp = parseInt(y);
  return (ap <= xp && yp <= bp) || (xp <= ap && bp <= yp);
}
console.log(_.sum(
  assignmentIntervals.map(elfIntervals => {
    const interval1 = elfIntervals[0].split("-"); const interval2 = elfIntervals[1].split("-");
    return (intervalContains(...interval1, ...interval2)) ? 1 : 0;
  })
));

function intervalOverlaps(a, b, x, y) {
  const ap = parseInt(a); const bp = parseInt(b); const xp = parseInt(x); const yp = parseInt(y);
  return (ap <= xp && xp <= bp) || (ap <= yp && yp <= bp) || (xp <= ap && ap <= yp) || (xp <= bp && bp <= yp);
}
console.log(_.sum(
  assignmentIntervals.map(elfIntervals => {
    const [interval1, interval2] = elfIntervals.map(someInt => someInt.split("-"));
    return (intervalOverlaps(...interval1, ...interval2)) ? 1 : 0;
  })
));
