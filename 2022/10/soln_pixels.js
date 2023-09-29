instructions = input.split("\n");

// part 1
var [total, reg, cyc] = [0, 1, 0];
function nextCyclePartOne() {
  cyc += 1;
  if ((cyc - 20) % 40 === 0) {
    // console.log(`adding ${reg*cyc} to ${total} for cycle ${cyc} and register ${reg}`);
    total += reg * cyc;
  }
}
instructions.forEach(inst => {
  nextCyclePartOne();
  if (inst === "noop") {
    return;
  }
  const loadval = parseInt(inst.split(" ")[1]);
  nextCyclePartOne();
  reg += loadval;
});
console.log(total)

// part 2
var [total, reg, cyc, row, soln] = [0, 1, 0, 0, ""];
function isSpriteActive(cycle, register) {
  var cycleIndex = (cycle - 1) % 40;
  const overlap = register === cycleIndex || register - 1 === cycleIndex || register + 1 == cycleIndex;
  // console.log(`${register} overlaps the pixel ${cycleIndex} on row {parseInt((cycle - 1) / 40)}`);
  return overlap;
}
function nextCyclePartTwo() {
  if (cyc % 40 === 0) {
    // console.log(`next row`);
    soln += "\n";
  }
  cyc += 1;
  if (isSpriteActive(cyc, reg)) {
    // console.log(`${reg} overlaps the pixel ${(cyc - 1)%40} on row ${parseInt((cyc - 1)/ 40)}`);
    soln += "#";
  } else {
    soln += ".";
  }
}
[total, reg, cyc, row, soln] = [0, 1, 0, 0, ""];
instructions.forEach(inst => {
  nextCyclePartTwo();
  if (inst === "noop") {
    return;
  }
  const loadval = parseInt(inst.split(" ")[1]);
  nextCyclePartTwo();
  reg += loadval;
}); 
console.log(soln);
