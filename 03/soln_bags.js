// part 1
var bagComps = input.split("\n").map(bag => {
  let bl = bag.length;
  let c1 = bag.substring(0, bl / 2);
  let c2 = bag.substring(bl / 2, bl);
  return [c1, c2]
});
var elements = bagComps.map(cs => _.intersection(...cs.map(e => e.split(""))));
console.log(
  _.sum(elements.map(e => {
    let cNum = e[0].charCodeAt();
    cNum = cNum > 96 ? cNum - 96 : cNum - 38
    return cNum;
  }))
);

// part 2
let elves = input.split("\n");
let groups = _.range(0, elves.length / 3).map(i => elves.slice(i*3, i*3 + 3));
const badges = groups.map(es => {
  return _.intersection(es[0].split(""), es[1].split(""), es[2].split(""));
});
console.log(
  _.sum(badges.map(e => {
    let cNum = e[0].charCodeAt();
    cNum = cNum > 96 ? cNum - 96 : cNum - 38
    return cNum;
  }))
);
