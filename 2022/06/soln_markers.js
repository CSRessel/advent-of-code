// part 1
const lastFour = input.split("").slice(0, 4);
input.split("").forEach((marker, index) => {
  if (index < 4) { return; }
  if ((new Set(lastFour)).size === 4) { console.log(index); lastFour.pop(); lastFour.pop(); lastFour.pop(); }
  lastFour.shift(); lastFour.push(marker);
});

// part 2
const buffer = input.split("").slice(0, 14);
input.split("").forEach((marker, index) => {
  if (index < 14) { return; }
  if ((new Set(buffer)).size === 14) { console.log(index); buffer.pop(); buffer.pop(); buffer.pop(); }
  buffer.shift(); buffer.push(marker);
});
