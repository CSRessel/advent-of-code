// manually transform input:
// JFCNDBW
// TSLQVZP
// TJGBZP
// CHBZJLTD
// SJBVG
// QSP
// NPMLFDVB
// RLDBFMSP
// RTDV

var stacks = input.split("\n").slice(0, 9);
stacks = stacks.map(s => s.split("").reverse().join(""));
var instructions = input.split("\n").slice(10, input.split("\n").length);

function makeMove(count, from, onto) {
  // console.log(`move ${count} from ${from} to ${onto}`);
  const fromIndex = from - 1; const ontoIndex = onto - 1;
  const stackHeight = stacks[fromIndex].length;
  const payload = stacks[fromIndex].substring(stackHeight - count, stackHeight);
  stacks[fromIndex] = stacks[fromIndex].substring(0, stackHeight - count);
  stacks[ontoIndex] += payload;
}

function makeMoveUpsideDown(count, from, onto) {
  // console.log(`move ${count} from ${from} to ${onto}`);
  const fromIndex = from - 1; const ontoIndex = onto - 1;
  const stackHeight = stacks[fromIndex].length;
  const payload = stacks[fromIndex].substring(stackHeight - count, stackHeight);
  stacks[fromIndex] = stacks[fromIndex].substring(0, stackHeight - count);
  stacks[ontoIndex] += payload.split("").reverse().join("");
}

// part 1
instructions.forEach(instruction => {
  var [m, count, f, from, t, onto] = instruction.split(" ");
  makeMoveUpsideDown(count, from, onto);
});
console.log(stacks.map(stack => stack.at(stack.length - 1)).join(""));

// part 2
stacks = input.split("\n").slice(0, 9);
stacks = stacks.map(s => s.split("").reverse().join(""));
instructions.forEach(instruction => {
  var [m, count, f, from, t, onto] = instruction.split(" ");
  makeMove(count, from, onto);
});
console.log(stacks.map(stack => stack.at(stack.length - 1)).join(""));

